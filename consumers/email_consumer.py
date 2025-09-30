from main import broker
from email_helper import send_message
from schemas.email_message import EmailMessage
from faststream.kafka.annotations import KafkaMessage
from faststream import Logger

@broker.subscriber('send-email-message',
                   auto_commit=False,
                   group_id='email',
                   description='Сюда подаются сообщения для отправки через email',
                   title='input_data:Consume_email_message')
async def send_email_consumer(body: EmailMessage, message: KafkaMessage, logger: Logger):
    await send_message(body)