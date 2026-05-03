from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.auth import (
    ResetPasswordRequest,
    SetNewPasswordRequest,
    SignInRequest,
    SignInResponse,
    SignUpRequest,
    SignUpResponse,
)
from app.models.core import BaseResponse
from app.services.authentication import AuthenticationService, get_authentication_service

router = APIRouter()


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(
    body: SignInRequest, auth_service: Annotated[AuthenticationService, Depends(get_authentication_service)]
) -> SignInResponse:
    return await auth_service.signin(body)


@router.post("/sign-up", response_model=SignUpResponse, status_code=201)
async def sign_up(
    body: SignUpRequest, auth_service: Annotated[AuthenticationService, Depends(get_authentication_service)]
) -> SignUpResponse:
    user = await auth_service.signup(body)
    return SignUpResponse(
        success=True,
        message="User registered successfully",
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
    )


@router.post("/reset-password", response_model=BaseResponse)
async def reset_password(body: ResetPasswordRequest) -> BaseResponse:
    raise NotImplementedError


@router.post("/set-new-password", response_model=BaseResponse)
async def set_new_password(body: SetNewPasswordRequest) -> BaseResponse:
    raise NotImplementedError
