from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio

from aiosmtplib import SMTP
from aiosmtplib.errors import (SMTPResponseException,
                               SMTPAuthenticationError,
                               SMTPConnectTimeoutError,
                               SMTPSenderRefused)

from logger_config import logger
from schemas.email_message import EmailMessage
from config import settings


async def send_message(message: EmailMessage):
    smtp_client = SMTP(
        hostname=settings.email.host,
        port=settings.email.port,
        use_tls=settings.email.ssl,
        start_tls=settings.email.starttls
    )
    try:
        await smtp_client.connect()
        if settings.email.username and settings.email.password:
            try:
                await smtp_client.login(settings.email.username,
                                    settings.email.password)
            except SMTPAuthenticationError:
                logger.error('Логин или пароль для подключения к почтовому'
                            ' серверу неверны или настройки сервера блокируют'
                            ' аутентификацию.')
                return
            
        prepared_message = MIMEMultipart('alternate')
        prepared_message['From'] = settings.email.sender
        prepared_message['To'] = ','.join(message.recipients)
        if message.subject:
            prepared_message['Subject'] = message.subject
        if message.plain:
            text_message = MIMEText(message.plain, 'plain', 'utf-8')
            prepared_message.attach(text_message)
        if message.html:
            html_message = MIMEText(message.html, 'html', 'utf-8')
            prepared_message.attach(html_message)
        try:
            await smtp_client.send_message(prepared_message)
        except SMTPSenderRefused:
            logger.error('Почтовый сервер отклонил сообщение с отправителем из настроек, '
                        'проверьте, что отправитель указан в формате логин@адрес_сервера')
        await smtp_client.quit()
    except SMTPConnectTimeoutError:
        logger.error('Соединение с почтовым сервером разорвано')
    except SMTPResponseException:
        logger.error('Код ответа сервера некорректен. Проверьте работу'
                     ' и настройки сервера.')