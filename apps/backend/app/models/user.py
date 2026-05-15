from pydantic import BaseModel, EmailStr, Field

from app.models.fields import Password


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    collection: list[str]


class ChangeProfileRequest(BaseModel):
    full_name: str = Field(min_length=1, description="The user's full name")


class AddCoindToCollectionRequest(BaseModel):
    record_id: str = Field(min_length=1, description="The OCRE record ID of the coin to add to the user's collection")


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: Password
