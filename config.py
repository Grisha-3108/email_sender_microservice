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
    server_connections: int = Field(qe=1, default=1)
    sender: EmailStr = 'root@localhost'
    username: str | None = None
    password: str | None = None

    @model_validator(mode='after')
    def none_password_for_none_user(self) -> Self:
        if self.username is None:
            self.password = None
        return self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        env_prefix='EMAIL_SENDER',
        case_sensitive=False,
        env_file_encoding='utf-8'
    )

    email: Email = Email()


settings = Settings()