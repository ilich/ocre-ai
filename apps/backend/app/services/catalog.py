from typing import Annotated, Any

from bson import ObjectId
from fastapi import Depends
from pydantic_ai import Embedder

from app.core.settings import Settings, get_settings
from app.models.catalog import CoinListResponse, CoinModel, FilterParams
from app.models.domain import Coin, Geographic

VECTOR_INDEX = "coins_vector_search"
TEXT_INDEX = "coins_text_search"

_SORT_FIELD: dict[str, str] = {
    "id": "record_id",
    "title": "title",
    "from_year": "from_year",
    "to_year": "to_year",
    "object_type": "object_type",
    "denomination": "denomination",
    "manufacturer": "manufacturer",
    "material": "material",
    "authority": "authority",
    "geographic": "geographic",
}


def _build_filter(params: FilterParams) -> dict[str, Any]:
    f: dict[str, Any] = {}
    if params.from_year is not None:
        f["from_year"] = {"$gte": params.from_year}
    if params.to_year is not None:
        f["to_year"] = {"$lte": params.to_year}
    if params.denomination:
        f["denomination"] = {"$in": params.denomination}
    if params.manufacturer:
        f["manufacturer"] = {"$in": params.manufacturer}
    if params.material:
        f["material"] = {"$in": params.material}
    if params.authority:
        f["authority"] = {"$in": params.authority}
    return f


def _map_coin(coin: Coin) -> CoinModel:
    return CoinModel(
        id=str(coin.record_id),
        title=coin.title,
        description=coin.description,
        object_type=coin.object_type,
        date_range=coin.date_range,
        denomination=coin.denomination,
        manufacturer=coin.manufacturer,
        material=coin.material,
        authority=coin.authority,
        geographic=[g.name for g in coin.geographic if isinstance(g, Geographic)],
        images=coin.images,
    )


class CatalogService:
    def __init__(self, config: Settings) -> None:
        self.config = config

    async def find_coins(self, params: FilterParams) -> CoinListResponse:
        if params.search:
            return await self._coins_search(params)
        return await self._list_coins(params)

    async def _coins_search(self, params: FilterParams) -> CoinListResponse:
        assert params.search
        embedder = Embedder(self.config.ai_embedding_model)
        embed_result = await embedder.embed_query(params.search)
        query_vector = embed_result.embeddings[0]

        collection = Coin.get_pymongo_collection()
        candidate_limit = max(100, params.skip + params.limit)
        mongo_filter = _build_filter(params)

        pipeline = [
            {
                "$rankFusion": {
                    "input": {
                        "pipelines": {
                            "vectorPipeline": [
                                {
                                    "$vectorSearch": {
                                        "index": VECTOR_INDEX,
                                        "path": "embedding",
                                        "queryVector": query_vector,
                                        "numCandidates": candidate_limit * 2,
                                        "limit": candidate_limit,
                                    }
                                }
                            ],
                            "textPipeline": [
                                {
                                    "$search": {
                                        "index": TEXT_INDEX,
                                        "text": {
                                            "query": params.search,
                                            "path": [
                                                "record_id",
                                                "title",
                                                "description",
                                                "authority",
                                                "denomination",
                                                "manufacturer",
                                                "material",
                                                "object_type",
                                            ],
                                        },
                                    }
                                },
                                {"$limit": candidate_limit},
                            ],
                        }
                    }
                }
            },
            *([{"$match": mongo_filter}] if mongo_filter else []),
            {
                "$facet": {
                    "items": [
                        {"$skip": params.skip},
                        {"$limit": params.limit},
                        {"$project": {"_id": 1}},
                    ],
                    "total": [{"$count": "count"}],
                }
            },
        ]
        cursor = await collection.aggregate(pipeline)
        rows = await cursor.to_list(length=1)

        facet = rows[0]
        total = facet["total"][0]["count"] if facet["total"] else 0
        page_ids = [str(doc["_id"]) for doc in facet["items"]]
        return CoinListResponse(items=await self._fetch_coins(page_ids), total=total)

    async def _list_coins(self, params: FilterParams) -> CoinListResponse:
        mongo_filter = _build_filter(params)
        query = Coin.find(mongo_filter, fetch_links=True)

        if params.order_by != "relevance":
            prefix = "" if params.order_direction == "asc" else "-"
            query = query.sort(f"{prefix}{_SORT_FIELD[params.order_by]}")

        total = await Coin.find(mongo_filter).count()
        coins = await query.skip(params.skip).limit(params.limit).to_list()
        return CoinListResponse(items=[_map_coin(coin) for coin in coins], total=total)

    async def _fetch_coins(self, ids: list[str]) -> list[CoinModel]:
        if not ids:
            return []

        object_ids = [ObjectId(id) for id in ids]
        coins_by_id = {
            str(coin.id): coin for coin in await Coin.find({"_id": {"$in": object_ids}}, fetch_links=True).to_list()
        }
        return [_map_coin(coins_by_id[id]) for id in ids if id in coins_by_id]


def get_catalog_service(
    config: Annotated[Settings, Depends(get_settings)],
) -> CatalogService:
    return CatalogService(config)
