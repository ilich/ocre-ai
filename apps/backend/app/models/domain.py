from datetime import datetime

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr


class ResetPasswordToken(BaseModel):
    token: str
    expires_at: datetime


class User(Document):
    full_name: str
    email: EmailStr = Indexed(unique=True)
    password: str
    created_at: datetime
    updated_at: datetime
    reset_password_tokens: list[ResetPasswordToken] = []

    class Settings:
        name = "users"
        indexes = [
            [("reset_password_tokens.token", 1), ("reset_password_tokens.expires_at", 1)],
        ]
