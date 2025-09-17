from faststream import FastStream
from faststream.kafka import KafkaBroker

from config import settings


broker = KafkaBroker(f'{settings.kafka.host}:{settings.kafka.port}')
app = FastStream(broker)