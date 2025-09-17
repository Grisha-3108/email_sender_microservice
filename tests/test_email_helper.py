from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytest

from email_helper import SMTP, send_message
from schemas.email_message import EmailMessage
from config import settings

@pytest.mark.asyncio
async def test_email_helper_correct_work(mocker):
    message = EmailMessage(recipients=['user@mail.ru'],
                           plain='Сообщение',
                           subject='Тема')
    async def check_message(self, prepared_message):
        assert prepared_message['From'] == settings.email.sender
        assert prepared_message['To'] == ','.join(message.recipients)
        assert prepared_message['Subject'] == message.subject
        assert prepared_message.get_payload()[0].get_payload() == '0KHQvtC+0LHRidC10L3QuNC1\n'
    mocker.patch.object(SMTP, 'send_message', check_message)
    mocked_smtp_quit = mocker.patch.object(SMTP, 'quit')
    mocked_smtp_connect = mocker.patch.object(SMTP, 'connect')
    
    await send_message(message)
    mocked_smtp_quit.assert_awaited_once()
    mocked_smtp_connect.assert_awaited_once()