from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from email.mime.text import MIMEText

from aiosmtplib import SMTP

from config import settings
from schemas import EmailInput

T = TypeVar("T")


class ISender(ABC, Generic[T]):
    @abstractmethod
    async def send(self, payload: T) -> None:
        pass


class EmailSender(ISender[EmailInput]):
    async def send(self, payload: EmailInput) -> None:
        sender_email = settings.email_sender
        recipient_email = settings.email_recipient
        message = MIMEText("html", "html")
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = payload.subject

        smtp = settings.smtp
        async with SMTP(
            hostname=smtp.smtp_host,
            port=smtp.smtp_port,
            use_tls=True,
        ) as smtp_client:
            await smtp_client.login(smtp.smtp_username, smtp.smtp_password)
            await smtp_client.send_message(message, sender=sender_email, recipients=[recipient_email])
