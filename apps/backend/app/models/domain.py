from datetime import datetime

from beanie import Document, Indexed
from pydantic import EmailStr


class User(Document):
    full_name: str
    email: EmailStr = Indexed(unique=True)
    password: str
    created_at: datetime
    updated_at: datetime

    class Settings:
        name = "users"
