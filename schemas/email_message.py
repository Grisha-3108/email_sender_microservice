from typing import Self

from pydantic import (BaseModel, 
                      EmailStr, 
                      model_validator)


class EmailMessage(BaseModel):
    recipients: list[EmailStr]
    subject: str | None = None
    plain: str | None = None
    html: str | None = None

    @model_validator(mode='after')
    def email_body_exists(self) -> Self:
        if (self.plain is None) and (self.html is None):
            raise ValueError('Сообщение должно содержать тело в виде текста plain или html')
        return self