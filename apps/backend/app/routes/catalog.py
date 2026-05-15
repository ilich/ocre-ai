from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

from app.models.catalog import CoinImageDescriptionResponse, CoinListResponse, CoinModel, FilterParams, MetadataModel
from app.models.domain import User
from app.services.authentication import get_current_user
from app.services.catalog import CatalogService, get_catalog_service
from app.services.vision import SupportedImageContentType, Vision, get_vision

router = APIRouter()

SUPPORTED_IMAGE_TYPES: dict[str, SupportedImageContentType] = {
    "image/png": "image/png",
    "image/jpeg": "image/jpeg",
}
SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


@router.get("", response_model=CoinListResponse)
async def find_coins(
    filter: Annotated[FilterParams, Depends(FilterParams)],
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CatalogService, Depends(get_catalog_service)],
    my: Annotated[bool, Query(description="Whether to search only in the user's collection")] = False,
) -> CoinListResponse:
    return await service.find_coins(filter, user if my else None)


@router.post("/image", response_model=CoinImageDescriptionResponse)
async def describe_coin_image(
    image: Annotated[UploadFile, File()],
    user: Annotated[User, Depends(get_current_user)],
    vision: Annotated[Vision, Depends(get_vision)],
) -> CoinImageDescriptionResponse:
    content_type = SUPPORTED_IMAGE_TYPES.get(image.content_type or "")
    filename = image.filename or ""
    has_supported_extension = any(filename.lower().endswith(extension) for extension in SUPPORTED_IMAGE_EXTENSIONS)
    if not content_type or not has_supported_extension:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PNG and JPG images are supported",
        )

    description = await vision.describe(await image.read(), content_type)
    return CoinImageDescriptionResponse(description=description)


@router.get("/metadata", response_model=list[MetadataModel])
async def get_metadata(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CatalogService, Depends(get_catalog_service)],
) -> list[MetadataModel]:
    return await service.get_coins_metadata()


@router.get("/{record_id}", response_model=CoinModel)
async def get_coin_by_id(
    record_id: str,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CatalogService, Depends(get_catalog_service)],
) -> CoinModel:
    coin = await service.get_coin_by_id(record_id)
    if not coin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coin not found")

    return coin
