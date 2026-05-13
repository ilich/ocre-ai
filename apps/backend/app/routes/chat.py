from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.chat import ChatRequest, ChatResponse
from app.models.domain import User
from app.services.authentication import get_current_user
from app.services.chat import ChatService, get_chat_service

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ChatService, Depends(get_chat_service)],
) -> ChatResponse:
    return await service.chat(request)
