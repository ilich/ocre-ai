from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.models.catalog import CoinListResponse, FilterParams
from app.models.domain import User
from app.services.authentication import get_current_user
from app.services.catalog import CatalogService, get_catalog_service

router = APIRouter()


@router.get("", response_model=CoinListResponse)
async def find_coins(
    filter: Annotated[FilterParams, Query()],
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CatalogService, Depends(get_catalog_service)],
) -> CoinListResponse:
    return await service.find_coins(filter)
