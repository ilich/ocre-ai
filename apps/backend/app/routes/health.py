from fastapi import APIRouter
from loguru import logger

from app.models.health import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health() -> HealthResponse:
    logger.debug("Health check endpoint called")
    return HealthResponse(status="ok")
