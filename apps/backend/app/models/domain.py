from datetime import datetime
from enum import StrEnum
from typing import Optional

from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr
from pymongo import ASCENDING, TEXT, IndexModel


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


class Geographic(Document):
    name: str
    type: str  # e.g. "mint", "findspot"

    class Settings:
        name = "geographics"
        indexes = [
            IndexModel([("name", ASCENDING), ("type", ASCENDING)], unique=True),
        ]


class Coin(Document):
    record_id: str
    title: str
    description: str | None
    object_type: str
    from_year: Optional[int] = None
    to_year: Optional[int] = None
    date_range: Optional[str] = None
    denomination: list[str] = []
    manufacturer: list[str] = []
    material: list[str] = []
    authority: list[str] = []
    geographic: list[Link[Geographic]] = []
    images: list[str] = []
    # text-embedding-3-small produces 1536-dimensional vectors
    # Atlas Vector Search index (create via Atlas UI / Admin API):
    # { "fields": [{ "type": "vector", "path": "embedding", "numDimensions": 1536, "similarity": "cosine" }] }
    embedding: Optional[list[float]] = None

    class Settings:
        name = "coins"
        indexes = [
            IndexModel([("record_id", ASCENDING)], unique=True),
            IndexModel([("from_year", ASCENDING)]),
            IndexModel([("to_year", ASCENDING)]),
            IndexModel([("denomination", ASCENDING)]),
            IndexModel([("manufacturer", ASCENDING)]),
            IndexModel([("material", ASCENDING)]),
            IndexModel([("authority", ASCENDING)]),
            IndexModel(
                [
                    ("title", TEXT),
                    ("description", TEXT),
                    ("denomination", TEXT),
                    ("manufacturer", TEXT),
                    ("material", TEXT),
                    ("authority", TEXT),
                ],
                name="coins_text_search",
            ),
        ]


class MetadataType(StrEnum):
    OBJECT_TYPE = "object_type"
    DENOMINATION = "denomination"
    MANUFACTURER = "manufacturer"
    MATERIAL = "material"
    AUTHORITY = "authority"


class Metadata(Document):
    type: MetadataType = Indexed()
    value: str

    class Settings:
        name = "metadata"
        indexes = [
            IndexModel([("type", ASCENDING), ("value", ASCENDING)], unique=True),
        ]
