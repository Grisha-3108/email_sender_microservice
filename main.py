from hashlib import sha256

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker
from faststream.kafka.annotations import KafkaMessage
from faststream.asyncapi.schema import Contact
from redis import ConnectionError

from redis_connection import redis_client
from config import settings
from logger_config import logger
from schemas.email_message import EmailMessage
from email_helper import send_message
from indempotence_consumer_middleware import IndempotenceConsumer

broker = KafkaBroker(f'{settings.kafka.host}:{settings.kafka.port}', 
                     enable_idempotence=True,
                     middlewares=[IndempotenceConsumer])

@broker.subscriber('send-email-message',
                   auto_commit=False,
                   group_id='email',
                   description='Сюда подаются сообщения для отправки через email',
                   title='input_data:Consume_email_message')
async def send_email_consumer(body: EmailMessage, message: KafkaMessage, logger: Logger):
    await send_message(body)


app = FastStream(broker,
                 title='Pet проект по отправке email',
                 version='1.0.0',
                 description='Приложение, которое отправляет email, полученные от брокера',
                 contact=Contact(name='Григорий Тихановский', email='Grisha-3108@yandex.ru')
                 )



@app.on_startup
async def startup():
    try:
        await redis_client.ping()
    except ConnectionError:
        logger.exception('Ошибка подключения к redis, проверьте настройки сервера и перезапустите'
                         ' приложение.')

@app.on_shutdown
async def shutdown():
    await redis_client.aclose()