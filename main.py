from faststream import FastStream
from faststream.kafka import KafkaBroker
import redis.asyncio as aioredis
from redis import ConnectionError

from config import settings
from logger_config import logger


broker = KafkaBroker(f'{settings.kafka.host}:{settings.kafka.port}')
app = FastStream(broker)

redis_client = None

@app.on_startup
async def startup():
    global redis_client
    redis_client = aioredis.Redis(host=settings.redis.host,
                                  port=settings.redis.port,
                                  db=settings.redis.db)
    try:
        await redis_client.ping()
    except ConnectionError:
        logger.exception('Ошибка подключения к redis, проверьте настройки сервера и перезапустите'
                         ' приложение.')

@app.on_shutdown
async def shutdown():
    await redis_client.close()