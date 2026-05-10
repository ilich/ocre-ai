from typing import Literal

from pydantic import BaseModel


class ChatHistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatAttachment(BaseModel):
    filename: str
    content_type: str
    data: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatHistoryItem] | None = None
    coins_context: list[str] | None = None
    attachment: ChatAttachment | None = None


class ChatResponse(BaseModel):
    message: str
