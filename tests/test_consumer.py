import pytest
from pytest import param
from faststream.kafka import TestKafkaBroker
from faststream import TestApp

from schemas.email_message import EmailMessage
from main import send_email_consumer
from logger_config import logger
from main import app

@pytest.mark.asyncio
@pytest.mark.parametrize('recipients, plain, html, subject',
                         [param(['user@mail.ru'], 'Сообщение', 
                               None, None, 
                               id='Only plain message with no subject and single user'),
                         param(['user@mail.ru', 'user2@mail.ru'], 'Сообщение', 
                               None, None, 
                               id='Only plain message with no subject and mulitply user'),
                         param(['user@mail.ru'], 'Сообщение', 
                               None, 'Тема', 
                               id='Only plain message with subject and single user'),
                         param(['user@mail.ru'], 'Сообщение', 
                               '<html><body>Сообщение</body></html>', 'Тема', 
                               id='Only both types of message with  subject and single user')
                         ]
                         )
async def test_send_message(clear_redis, mocker, recipients, plain, html, subject):
    async with TestKafkaBroker(app.broker, with_real=True) as kafka_broker, TestApp(app):
      message = EmailMessage(recipients=recipients,
                              plain=plain,
                              html=html,
                              subject=subject)
      mocked_send_message = mocker.patch('main.send_message')
      await kafka_broker.publish(message, topic='send-email-message')
      await send_email_consumer.wait_call(timeout=3)
      mocked_send_message.assert_awaited_once_with(message)