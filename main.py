from hashlib import sha256

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker
from faststream.kafka.annotations import KafkaMessage
from redis import ConnectionError

from redis_connection import redis_client
from config import settings
from logger_config import logger
from schemas.email_message import EmailMessage
from email_helper import send_message


broker = KafkaBroker(f'{settings.kafka.host}:{settings.kafka.port}')
@broker.subscriber('send-email-message',
                   auto_commit=False,
                   group_id='email',
                   description='Сюда подаются сообщения для отправки через email',
                   title='input_data:Consume_email_message')
async def send_email_consumer(body: EmailMessage, message: KafkaMessage, logger: Logger):
    message_hash = sha256(message.body).digest()
    if key:=await redis_client.get(message_hash) != b'1':
        await send_message(body)
        res = await redis_client.setex(message_hash,
                                    settings.kafka.duplicate_cache_time,
                                    b'1')
        logger.debug('Ключ получен: %s, Ключ был добавлен: %s', key, res)

app = FastStream(broker,
                 title='Pet проект по отправке email',
                 version='1.0.0',
                 description='Приложение, которое отправляет email, полученные от брокера',
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