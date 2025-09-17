import logging

from redis_connection import redis_client
from schemas.email_message import EmailMessage
from email_helper import send_message
from config import settings
from logger_config import logger


async def send_email_consumer(body: EmailMessage):
        print(f'Потребитель send_email_consumer получил сообщение: {body.model_dump_json()}')
    # if key:=await redis_client.get(body.model_dump_json()) != b'1':
    #     await send_message(body)
    #     res = await redis_client.setex(body.model_dump_json(),
    #                                 settings.kafka.duplicate_cache_time,
    #                                 b'1')
    #     logger.debug('Ключ получен: %s, Ключ был добавлен: %s', key, res)