from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from loguru import logger

from app.core.settings import Settings, get_settings
from app.models.auth import SignInRequest, SignInResponse, SignUpRequest
from app.models.domain import User
from app.services.user_repository import UserRepository, get_user_repository

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"


class AuthenticationService:
    def __init__(self, user_repository: UserRepository, config: Settings):
        self.users = user_repository
        self.config = config

    async def signup(self, request: SignUpRequest) -> User:
        request.email = request.email.strip().lower()
        existing_user = await self.users.get_user_by_email(request.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered")

        try:
            ph = PasswordHasher()
            hashed_password = ph.hash(request.password)
            new_user = await self.users.create_user(
                email=request.email, password=hashed_password, full_name=request.full_name
            )
            logger.info(f"New user registered: {new_user.email} (ID: {new_user.id})")
            return new_user
        except Exception as e:
            logger.error(f"Error during user registration: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User registration failed")

    async def signin(self, request: SignInRequest) -> SignInResponse:
        login = request.login.strip().lower()
        user = await self.users.get_user_by_email(login)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        ph = PasswordHasher()
        try:
            ph.verify(user.password, request.password)
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({"user_id": str(user.id), "exp": expiration}, self.config.secret_key, algorithm=ALGORITHM)
        return SignInResponse(access_token=token, token_type="bearer")


def get_authentication_service(
    users: Annotated[UserRepository, Depends(get_user_repository)], config: Annotated[Settings, Depends(get_settings)]
) -> AuthenticationService:
    return AuthenticationService(users, config)
