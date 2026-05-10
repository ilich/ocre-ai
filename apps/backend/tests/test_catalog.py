import asyncio
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

from bson import ObjectId

from app.core.settings import Settings
from app.models.catalog import CoinListResponse, FilterParams
from app.models.domain import Coin, Geographic
from app.services.catalog import CatalogService, _build_filter, _map_coin

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _settings() -> Settings:
    return Settings(
        mongodb_uri="mongodb://localhost:27017",
        mongodb_database="test",
        secret_key="test-secret-key",
        public_url="http://localhost",
        email_from="test@test.com",
        smtp_host="localhost",
        smtp_port=25,
        openai_api_key="test-key",
        ai_model="gpt-4o",
        ai_embedding_model="text-embedding-3-small",
    )


def _service() -> CatalogService:
    return CatalogService(_settings())


def _make_coin(**kwargs: Any) -> SimpleNamespace:
    defaults = dict(
        id=ObjectId(),
        record_id="rrc.1.1",
        title="Test Coin",
        description="A test description",
        object_type="Coin",
        date_range=None,
        denomination=["denarius"],
        manufacturer=[],
        material=["silver"],
        authority=["Augustus"],
        geographic=[],
        images=["img.jpg"],
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _mock_find_query(coins: list[Any] | None = None, count: int = 0) -> MagicMock:
    query = MagicMock()
    query.sort = MagicMock(return_value=query)
    query.skip = MagicMock(return_value=query)
    query.limit = MagicMock(return_value=query)
    query.to_list = AsyncMock(return_value=coins or [])
    query.count = AsyncMock(return_value=count)
    return query


def _mock_collection(facet_items: list[Any] | None = None, total: int = 0) -> MagicMock:
    cursor = AsyncMock()
    cursor.to_list = AsyncMock(
        return_value=[
            {
                "items": facet_items or [],
                "total": [{"count": total}] if total else [],
            }
        ]
    )
    collection = MagicMock()
    collection.aggregate = AsyncMock(return_value=cursor)
    return collection


def _mock_embedder(vector: list[float] | None = None) -> MagicMock:
    embed_result = MagicMock()
    embed_result.embeddings = [vector or [0.1] * 5]
    embedder = MagicMock()
    embedder.embed_query = AsyncMock(return_value=embed_result)
    return embedder


# ---------------------------------------------------------------------------
# _build_filter
# ---------------------------------------------------------------------------


def test_build_filter_empty_when_no_params() -> None:
    assert _build_filter(FilterParams()) == {}


def test_build_filter_from_year() -> None:
    assert _build_filter(FilterParams(from_year=100)) == {"from_year": {"$gte": 100}}


def test_build_filter_to_year() -> None:
    assert _build_filter(FilterParams(to_year=400)) == {"to_year": {"$lte": 400}}


def test_build_filter_denomination() -> None:
    result = _build_filter(FilterParams(denomination=["denarius", "aureus"]))
    assert result == {"denomination": {"$in": ["denarius", "aureus"]}}


def test_build_filter_material() -> None:
    assert _build_filter(FilterParams(material=["silver"])) == {"material": {"$in": ["silver"]}}


def test_build_filter_manufacturer() -> None:
    assert _build_filter(FilterParams(manufacturer=["Rome"])) == {"manufacturer": {"$in": ["Rome"]}}


def test_build_filter_authority() -> None:
    assert _build_filter(FilterParams(authority=["Augustus"])) == {"authority": {"$in": ["Augustus"]}}


def test_build_filter_empty_lists_not_included() -> None:
    params = FilterParams(denomination=[], manufacturer=[], material=[], authority=[])
    assert _build_filter(params) == {}


def test_build_filter_multiple_filters_combined() -> None:
    params = FilterParams(from_year=100, to_year=400, material=["silver"], authority=["Augustus"])
    assert _build_filter(params) == {
        "from_year": {"$gte": 100},
        "to_year": {"$lte": 400},
        "material": {"$in": ["silver"]},
        "authority": {"$in": ["Augustus"]},
    }


# ---------------------------------------------------------------------------
# _map_coin
# ---------------------------------------------------------------------------


def test_map_coin_maps_basic_fields() -> None:
    coin = _make_coin()
    result = _map_coin(coin)  # type: ignore[arg-type]
    assert result.id == "rrc.1.1"
    assert result.title == "Test Coin"
    assert result.description == "A test description"
    assert result.object_type == "Coin"
    assert result.denomination == ["denarius"]
    assert result.material == ["silver"]
    assert result.images == ["img.jpg"]


def test_map_coin_resolves_geographic_links() -> None:
    geo = MagicMock(spec=Geographic)
    geo.name = "Rome"
    geo.type = "mint"
    coin = _make_coin(geographic=[geo])
    result = _map_coin(coin)  # type: ignore[arg-type]
    assert result.geographic == ["Rome"]


def test_map_coin_excludes_unresolved_geographic_links() -> None:
    # Un-fetched links come back as raw Link objects, not Geographic instances
    coin = _make_coin(geographic=[MagicMock()])
    result = _map_coin(coin)  # type: ignore[arg-type]
    assert result.geographic == []


# ---------------------------------------------------------------------------
# find_coins dispatch
# ---------------------------------------------------------------------------


def test_find_coins_dispatches_to_coins_search_when_search_provided() -> None:
    service = _service()
    params = FilterParams(search="roman")
    mock_hybrid = AsyncMock(return_value=CoinListResponse(items=[], total=0))
    mock_list = AsyncMock(return_value=CoinListResponse(items=[], total=0))
    with patch.object(service, "_coins_search", new=mock_hybrid), patch.object(service, "_list_coins", new=mock_list):
        asyncio.run(service.find_coins(params))
    mock_hybrid.assert_awaited_once_with(params)
    mock_list.assert_not_called()


def test_find_coins_dispatches_to_list_coins_when_no_search() -> None:
    service = _service()
    params = FilterParams()
    mock_hybrid = AsyncMock(return_value=CoinListResponse(items=[], total=0))
    mock_list = AsyncMock(return_value=CoinListResponse(items=[], total=0))
    with patch.object(service, "_coins_search", new=mock_hybrid), patch.object(service, "_list_coins", new=mock_list):
        asyncio.run(service.find_coins(params))
    mock_list.assert_awaited_once_with(params)
    mock_hybrid.assert_not_called()


# ---------------------------------------------------------------------------
# _list_coins
# ---------------------------------------------------------------------------


def test_list_coins_returns_coin_list_response() -> None:
    service = _service()
    coin = _make_coin()
    with patch.object(Coin, "find", return_value=_mock_find_query(coins=[coin], count=1)):
        result = asyncio.run(service._list_coins(FilterParams()))
    assert isinstance(result, CoinListResponse)
    assert result.total == 1
    assert len(result.items) == 1
    assert result.items[0].id == "rrc.1.1"


def test_list_coins_passes_filter_to_find() -> None:
    service = _service()
    params = FilterParams(material=["silver"])
    with patch.object(Coin, "find") as mock_find:
        mock_find.return_value = _mock_find_query()
        asyncio.run(service._list_coins(params))
    for call in mock_find.call_args_list:
        assert call.args[0] == {"material": {"$in": ["silver"]}}


def test_list_coins_applies_sort() -> None:
    service = _service()
    mock_query = _mock_find_query()
    with patch.object(Coin, "find", return_value=mock_query):
        asyncio.run(service._list_coins(FilterParams(order_by="title", order_direction="desc")))
    mock_query.sort.assert_called_once_with("-title")


def test_list_coins_no_sort_when_order_by_relevance() -> None:
    service = _service()
    mock_query = _mock_find_query()
    with patch.object(Coin, "find", return_value=mock_query):
        asyncio.run(service._list_coins(FilterParams(order_by="relevance")))
    mock_query.sort.assert_not_called()


def test_list_coins_ascending_sort() -> None:
    service = _service()
    mock_query = _mock_find_query()
    with patch.object(Coin, "find", return_value=mock_query):
        asyncio.run(service._list_coins(FilterParams(order_by="from_year", order_direction="asc")))
    mock_query.sort.assert_called_once_with("from_year")


# ---------------------------------------------------------------------------
# _coins_search
# ---------------------------------------------------------------------------


def test_coins_search_calls_embedder_with_search_text() -> None:
    service = _service()
    embedder = _mock_embedder()
    with (
        patch("app.services.catalog.Embedder", return_value=embedder),
        patch.object(Coin, "get_pymongo_collection", return_value=_mock_collection()),
        patch.object(Coin, "find", return_value=_mock_find_query()),
    ):
        asyncio.run(service._coins_search(FilterParams(search="roman")))
    embedder.embed_query.assert_awaited_once_with("roman")


def test_coins_search_includes_match_stage_when_filters_set() -> None:
    service = _service()
    mock_col = _mock_collection()
    with (
        patch("app.services.catalog.Embedder", return_value=_mock_embedder()),
        patch.object(Coin, "get_pymongo_collection", return_value=mock_col),
        patch.object(Coin, "find", return_value=_mock_find_query()),
    ):
        asyncio.run(service._coins_search(FilterParams(search="roman", material=["silver"])))
    pipeline = mock_col.aggregate.call_args.args[0]
    match_stages = [s for s in pipeline if "$match" in s]
    assert len(match_stages) == 1
    assert match_stages[0]["$match"] == {"material": {"$in": ["silver"]}}


def test_coins_search_excludes_match_stage_when_no_filters() -> None:
    service = _service()
    mock_col = _mock_collection()
    with (
        patch("app.services.catalog.Embedder", return_value=_mock_embedder()),
        patch.object(Coin, "get_pymongo_collection", return_value=mock_col),
        patch.object(Coin, "find", return_value=_mock_find_query()),
    ):
        asyncio.run(service._coins_search(FilterParams(search="roman")))
    pipeline = mock_col.aggregate.call_args.args[0]
    assert not any("$match" in s for s in pipeline)


def test_coins_search_returns_coin_list_response() -> None:
    service = _service()
    oid = ObjectId()
    coin = _make_coin(id=oid)
    mock_col = _mock_collection(facet_items=[{"_id": oid}], total=1)
    with (
        patch("app.services.catalog.Embedder", return_value=_mock_embedder()),
        patch.object(Coin, "get_pymongo_collection", return_value=mock_col),
        patch.object(Coin, "find", return_value=_mock_find_query(coins=[coin], count=1)),
    ):
        result = asyncio.run(service._coins_search(FilterParams(search="roman")))
    assert isinstance(result, CoinListResponse)
    assert result.total == 1
    assert len(result.items) == 1


def test_coins_search_returns_empty_when_no_results() -> None:
    service = _service()
    mock_col = _mock_collection(facet_items=[], total=0)
    with (
        patch("app.services.catalog.Embedder", return_value=_mock_embedder()),
        patch.object(Coin, "get_pymongo_collection", return_value=mock_col),
        patch.object(Coin, "find", return_value=_mock_find_query()),
    ):
        result = asyncio.run(service._coins_search(FilterParams(search="roman")))
    assert result.total == 0
    assert result.items == []


# ---------------------------------------------------------------------------
# _fetch_coins
# ---------------------------------------------------------------------------


def test_fetch_coins_returns_empty_for_empty_ids() -> None:
    result = asyncio.run(_service()._fetch_coins([]))
    assert result == []


def test_fetch_coins_preserves_rrf_order() -> None:
    id1, id2 = ObjectId(), ObjectId()
    coin1 = _make_coin(id=id1, record_id="rrc.1.1")
    coin2 = _make_coin(id=id2, record_id="rrc.2.1")
    # DB returns [coin1, coin2] but we request [id2, id1] — result must follow the requested order
    with patch.object(Coin, "find", return_value=_mock_find_query(coins=[coin1, coin2])):
        result = asyncio.run(_service()._fetch_coins([str(id2), str(id1)]))
    assert result[0].id == "rrc.2.1"
    assert result[1].id == "rrc.1.1"


def test_fetch_coins_skips_missing_ids() -> None:
    oid = ObjectId()
    ghost_id = str(ObjectId())
    coin = _make_coin(id=oid)
    with patch.object(Coin, "find", return_value=_mock_find_query(coins=[coin])):
        result = asyncio.run(_service()._fetch_coins([str(oid), ghost_id]))
    assert len(result) == 1
    assert result[0].id == "rrc.1.1"
