from faststream import FastStream
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
                   group_id='email')
async def send_email_consumer(body: EmailMessage, message: KafkaMessage):
    if key:=await redis_client.get(message.message_id) != b'1':
        await send_message(body)
        res = await redis_client.setex(message.message_id,
                                    settings.kafka.duplicate_cache_time,
                                    b'1')
        logger.debug('Ключ получен: %s, Ключ был добавлен: %s', key, res)
    await message.ack()
app = FastStream(broker)



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