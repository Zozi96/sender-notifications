from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from aiosmtplib import SMTP
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import settings
from schemas import EmailInput

T = TypeVar("T")


class ISender(ABC, Generic[T]):
    @abstractmethod
    async def send(self, payload: T) -> None:
        pass


class EmailSender(ISender[EmailInput]):
    def __init__(self) -> None:
        templates_dir = Path(__file__).resolve().parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.logo_path = Path(__file__).resolve().parent / "static" / "zozbit.png"

    async def send(self, payload: EmailInput) -> None:
        sender_email = settings.email_sender
        recipient_email = settings.email_recipient
        html_body = self._render_html(payload)
        text_body = self._render_text(payload)

        message = MIMEMultipart("related")
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = payload.subject

        message_alternative = MIMEMultipart("alternative")
        message.attach(message_alternative)

        message_alternative.attach(MIMEText(text_body, "plain", "utf-8"))
        message_alternative.attach(MIMEText(html_body, "html", "utf-8"))

        if self.logo_path.exists():
            with open(self.logo_path, "rb") as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                image.add_header("Content-ID", "<zozbit_logo>")
                image.add_header("Content-Disposition", "inline", filename="zozbit.png")
                message.attach(image)

        smtp = settings.smtp
        async with SMTP(
            hostname=smtp.smtp_host,
            port=smtp.smtp_port,
            use_tls=smtp.smtp_use_tls,
        ) as smtp_client:
            await smtp_client.login(smtp.smtp_username, smtp.smtp_password)
            await smtp_client.send_message(
                message, sender=sender_email, recipients=[recipient_email]
            )

    def _render_html(self, payload: EmailInput) -> str:
        template_vars = self._template_variables(payload)

        try:
            template = self.jinja_env.get_template("notification.html")
            return template.render(**template_vars)
        except Exception:
            body = template_vars.get("body", "")
            return (
                "<!DOCTYPE html>"
                '<html lang="en">'
                '<head><meta charset="utf-8"></head>'
                '<body style="font-family: Arial, sans-serif; color: #0f172a;">'
                f'<div style="max-width: 600px; margin: 0 auto;">{body}</div>'
                "</body>"
                "</html>"
            )

    def _render_text(self, payload: EmailInput) -> str:
        if payload.preview_text:
            return payload.preview_text
        return payload.template_variables.body

    def _template_variables(self, payload: EmailInput) -> dict[str, str]:
        template_vars = payload.template_variables.model_dump()
        template_vars["subject"] = payload.subject
        if payload.preview_text:
            template_vars["preview_text"] = payload.preview_text
        return {k: str(v) if v is not None else "" for k, v in template_vars.items()}
