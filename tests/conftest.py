import pytest_asyncio
from faststream import TestApp
from faststream.kafka import TestKafkaBroker

from main import broker, app
from logger_config import logger
from redis_connection import redis_client

@pytest_asyncio.fixture(scope='session')
async def clear_redis():
    await redis_client.flushdb()


@pytest_asyncio.fixture(scope='function')
async def kafka_broker(clear_redis):
    async with TestApp(app):
        async with TestKafkaBroker(broker) as br:
            yield br