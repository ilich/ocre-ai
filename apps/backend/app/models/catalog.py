from typing import Literal

from pydantic import BaseModel


class FilterParams(BaseModel):
    search: str | None = None
    from_year: int | None = None
    to_year: int | None = None
    denomination: list[str] = []
    manufacturer: list[str] = []
    material: list[str] = []
    authority: list[str] = []
    order_by: Literal[
        "relevance",
        "id",
        "title",
        "from_year",
        "to_year",
        "object_type",
        "denomination",
        "manufacturer",
        "material",
        "authority",
        "geographic",
    ] = "relevance"
    order_direction: Literal["asc", "desc"] = "asc"
    skip: int = 0
    limit: int = 25


class CoinModel(BaseModel):
    id: str
    title: str
    description: str | None
    object_type: str
    date_range: str | None
    denomination: list[str] = []
    manufacturer: list[str] = []
    material: list[str] = []
    authority: list[str] = []
    geographic: list[str] = []
    images: list[str] = []


class CoinListResponse(BaseModel):
    items: list[CoinModel]
    total: int


class CoinImageDescriptionResponse(BaseModel):
    description: str


class MetadataModel(BaseModel):
    key: str
    values: list[str]

