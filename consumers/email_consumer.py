from typing import List

from main import broker
from schemas.email_message import EmailMessage
from email_helper import send_message

@broker.subscriber('send-email-message', 
                   auto_commit=False,
                   batch=True)
async def send_email_consumer(bodies: List[EmailMessage]):
    for body in bodies:
        
        await send_message(body)