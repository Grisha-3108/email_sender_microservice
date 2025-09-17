import redis.asyncio as aioredis
from config import settings

redis_client = redis_client = aioredis.Redis(host=settings.redis.host,
                                  port=settings.redis.port,
                                  db=settings.redis.db)