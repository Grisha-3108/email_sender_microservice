import pytest_asyncio
from faststream import TestApp
from faststream.kafka import TestKafkaBroker

from main import app
from redis_connection import redis_client

@pytest_asyncio.fixture(scope='session')
async def clear_redis():
    await redis_client.flushdb()


@pytest_asyncio.fixture(scope='session')
async def test_app(clear_redis):
    async with TestApp(app) as ta:
            yield ta