from fastapi import APIRouter, Depends

from app.models.core import BaseResponse
from app.models.domain import User
from app.models.user import ChangePasswordRequest, UserResponse
from app.services.authentication import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_profile(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
    )


@router.post("/change-password", response_model=BaseResponse)
async def change_password(body: ChangePasswordRequest) -> BaseResponse:
    raise NotImplementedError
