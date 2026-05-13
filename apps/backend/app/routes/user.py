from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.core import BaseResponse
from app.models.domain import User
from app.models.user import AddCoindToCollectionRequest, ChangePasswordRequest, UserResponse
from app.services.authentication import get_current_user
from app.services.user_repository import UserRepository, get_user_repository

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_profile(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        collection=user.collection,
    )


@router.post("/change-password", response_model=BaseResponse)
async def change_password(
    body: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> BaseResponse:
    ph = PasswordHasher()
    try:
        ph.verify(user.password, body.old_password)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")

    user.password = ph.hash(body.new_password)
    await user_repository.update_user(user)
    return BaseResponse(success=True)


@router.post("/collection", response_model=BaseResponse)
async def add_coin_to_collection(
    body: AddCoindToCollectionRequest,
    user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> BaseResponse:
    await user_repository.add_coin_to_collection(user, body.record_id)
    return BaseResponse(success=True)


@router.delete("/collection/{record_id}", response_model=BaseResponse)
async def remove_coin_from_collection(
    record_id: str,
    user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> BaseResponse:
    await user_repository.remove_coin_from_collection(user, record_id)
    return BaseResponse(success=True)
