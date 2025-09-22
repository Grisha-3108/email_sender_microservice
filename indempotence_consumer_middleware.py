from typing import Any
from hashlib import sha256

from faststream import BaseMiddleware
from faststream.broker.message import StreamMessage
from faststream.exceptions import AckMessage

from redis_connection import redis_client
from config import settings

class IndempotenceConsumer(BaseMiddleware):
    async def consume_scope(self, call_next, msg: StreamMessage[Any]):
        message_hash = sha256(msg.body).digest()
        if key:=await redis_client.get(message_hash) != b'1':
            res = await call_next(msg)
            await redis_client.setex(message_hash, settings.kafka.duplicate_cache_time, b'1')
        else:
            raise AckMessage()
        return res