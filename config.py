from typing import Self

from pydantic_settings import (BaseSettings, 
                               SettingsConfigDict)
from pydantic import (BaseModel, 
                      Field, 
                      EmailStr, 
                      model_validator)



class Email(BaseModel):
    host: str = 'localhost'
    port: int = Field(qe = 0, le=65535, default=587)
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
    port: int = Field(qe=0, le=65535, default=9092)


class Settings(BaseSettings):
    email: Email = Email()
    kafka: Kafka = Kafka()

    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        env_prefix='EMAIL_SENDER__',
        case_sensitive=False,
        env_file_encoding='utf-8'
    )

settings = Settings()