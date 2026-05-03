from fastapi import APIRouter

from app.models.core import BaseResponse
from app.models.user import ChangePasswordRequest, User

router = APIRouter()


@router.get("/me", response_model=User)
async def get_current_user() -> User:
    return User(
        id=1,
        email="test@example.com",
        full_name="John Doe",
    )


@router.post("/change-password", response_model=BaseResponse)
async def change_password(body: ChangePasswordRequest) -> BaseResponse:
    raise NotImplementedError
