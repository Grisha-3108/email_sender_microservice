from typing import List

from main import broker, redis_client
from schemas.email_message import EmailMessage
from email_helper import send_message
from config import settings


@broker.subscriber('send-email-message', 
                   auto_commit=False,
                   batch=True)
async def send_email_consumer(bodies: List[EmailMessage]):
    for body in bodies:
        if await redis_client.get(body.model_dump_json()) != b'1':
            await send_message(body)
            await redis_client.setex(body.model_dump_json(),
                                     settings.kafka.duplicate_cache_time,
                                     b'1')