from pydantic import BaseModel, EmailStr, Field

from app.models.core import BaseResponse
from app.models.fields import Password


class SignInRequest(BaseModel):
    login: EmailStr
    password: str


class SignInResponse(BaseModel):
    access_token: str
    token_type: str


class SignUpRequest(BaseModel):
    email: EmailStr
    password: Password
    full_name: str = Field(..., min_length=2)


class SignUpResponse(BaseResponse):
    id: str
    email: EmailStr
    full_name: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class SetNewPasswordRequest(BaseModel):
    token: str
    new_password: Password
