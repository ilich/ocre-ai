from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.core import BaseResponse
from app.models.fields import Password


class SignInRequest(BaseModel):
    login: EmailStr
    password: str


class SignInResponse(BaseResponse):
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class SignUpRequest(BaseModel):
    email: EmailStr
    password: Password
    full_name: str = Field(..., min_length=2)


class SignUpResponse(BaseResponse):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class SetNewPasswordRequest(BaseModel):
    token: str
    new_password: Password
