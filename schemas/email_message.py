from typing import Self

from pydantic import (BaseModel, 
                      EmailStr, 
                      model_validator,
                      ConfigDict,
                      Field)


class EmailMessage(BaseModel):
    recipients: list[EmailStr] = Field(
        json_schema_extra={'description': 'email-адреса получателей сообщений', 
                           'examples': ['user@mail.ru']})
    subject: str | None = Field(json_schema_extra={
            'description': 'Тема отправляемого сообщения',
            'examples': ['Тема сообщения'],
            'default': None
        }, default=None)
    plain: str | None = Field(json_schema_extra={
        'description': 'Тело email-сообщения в виде текста',
        'examples': ['сообщение'],
        'default': None
    }, default=None)
    html: str | None = Field(json_schema_extra={
        'description': 'Тело email-сообщения в виде html',
        'examples': ['<html><body><p>сообщение</p></body></html>'],
        'default': None
    }, default=None)

    @model_validator(mode='after')
    def email_body_exists(self) -> Self:
        if (self.plain is None) and (self.html is None):
            raise ValueError('Сообщение должно содержать тело в виде текста plain или html')
        return self
    
    model_config = ConfigDict(
        json_schema_extra={'description': 'Модель для email-сообщения как в текстовом, так и в html-виде'},
        extra='forbid'
        )