from typing import Self, Annotated
from annotated_types import Le
from pathlib import Path

from pydantic_settings import (BaseSettings, 
                               SettingsConfigDict)
from pydantic import (BaseModel,
                      EmailStr, 
                      model_validator,
                      NonNegativeInt,
                      PositiveInt)

BASE_DIR = Path(__file__).resolve().parent


class Email(BaseModel):
    host: str = 'localhost'
    port: Annotated[NonNegativeInt, Le(le=65535)] = 587
    sender: EmailStr = 'root@localhost'
    username: str | None = None
    password: str | None = None
    ssl: bool = False
    starttls: bool = False

    @model_validator(mode='after')
    def none_password_for_none_user(self) -> Self:
        if self.username is None:
            self.password = None
        return self
    
class Kafka(BaseModel):
    host: str = 'localhost'
    port: Annotated[NonNegativeInt, Le(le=65535)] = 9092
    duplicate_cache_time: PositiveInt = 60

class Redis(BaseModel):
    host: str = 'localhost'
    port: Annotated[NonNegativeInt, Le(le=65535)] = 6379
    db: NonNegativeInt = 0


class Settings(BaseSettings):
    email: Email = Email()
    kafka: Kafka = Kafka()
    redis: Redis = Redis()

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_nested_delimiter='__',
        env_prefix='EMAIL_SENDER__',
        case_sensitive=False,
        env_file_encoding='utf-8'
    )

settings = Settings()