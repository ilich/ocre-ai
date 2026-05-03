from typing import Annotated

from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status

from app.models.auth import SignUpRequest
from app.models.domain import User
from app.services.user_repository import UserRepository, get_user_repository


class AuthenticationService:
    def __init__(self, user_repository):
        self.users = user_repository

    async def signup(self, request: SignUpRequest) -> User:
        request.email = request.email.strip().lower()
        existing_user = await self.users.get_user_by_email(request.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered")

        ph = PasswordHasher()
        hashed_password = ph.hash(request.password)
        new_user = await self.users.create_user(
            email=request.email, password=hashed_password, full_name=request.full_name
        )
        return new_user


def get_authentication_service(users: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthenticationService:
    return AuthenticationService(users)
