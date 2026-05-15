import smtplib
from email.mime.text import MIMEText

import jinja2
from fastapi import Depends

from app.core.settings import Settings, get_settings
from app.models.domain import User


class EmailService:
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.settings = settings
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("app/templates"))

    def send_forgot_password_email(self, user: User, token: str) -> None:
        reset_password_url = f"{self.settings.public_url}/reset-password/{token}"
        subject = "Reset Your Password"
        template = self.jinja_env.get_template("forgot_password.html")
        body = template.render(user=user, reset_password_url=reset_password_url)
        self.send_email(user.email, subject, body)

    def send_email(self, to_email: str, subject: str, body: str) -> None:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = self.settings.email_from
        msg["To"] = to_email

        with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port) as server:
            if self.settings.smtp_use_tls:
                server.starttls()

            if self.settings.smtp_username and self.settings.smtp_password:
                server.login(self.settings.smtp_username, self.settings.smtp_password)
            server.send_message(msg)


def get_email_service(settings: Settings = Depends(get_settings)) -> EmailService:
    return EmailService(settings)
