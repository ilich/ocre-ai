from pydantic import BaseModel, EmailStr

from app.models.fields import Password


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: Password
