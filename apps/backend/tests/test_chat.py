import asyncio
import base64
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.core.settings import Settings
from app.models.catalog import CoinModel
from app.models.chat import ChatAttachment, ChatRequest
from app.services.catalog import CatalogService
from app.services.chat import ChatService, _create_agent, _Deps, _validated_attachment_content_type
from app.services.vision import Vision

MOCK_LLM_MODEL = "test"


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
        ai_model=MOCK_LLM_MODEL,
        ai_embedding_model="text-embedding-3-small",
    )


def test_validated_attachment_content_type_accepts_supported_images() -> None:
    assert _validated_attachment_content_type("image/png") == "image/png"
    assert _validated_attachment_content_type("image/jpeg") == "image/jpeg"


def test_validated_attachment_content_type_rejects_unsupported_images() -> None:
    with pytest.raises(HTTPException) as exc_info:
        _validated_attachment_content_type("image/gif")

    assert exc_info.value.status_code == 415
    assert exc_info.value.detail == "Only PNG and JPG images are supported"


def test_chat_rejects_unsupported_attachment_before_creating_agent() -> None:
    service = ChatService(_settings())
    request = ChatRequest(
        message="Identify this coin",
        attachment=ChatAttachment(filename="coin.gif", content_type="image/gif", data="Z2lmLWJ5dGVz"),
    )

    with patch("app.services.chat._get_agent") as get_agent:
        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(service.chat(request))

    assert exc_info.value.status_code == 415
    get_agent.assert_not_called()


def test_chat_resolves_coin_context_record_ids_before_agent_run() -> None:
    service = ChatService(_settings())
    request = ChatRequest(message="Compare these coins", coins_context=["rrc.1.1", "missing.id"])
    catalog = MagicMock(spec=CatalogService)
    catalog.find_coins_by_record_ids = AsyncMock(
        return_value=[
            CoinModel(
                id="rrc.1.1",
                title="Test Coin",
                description="A test coin description",
                object_type="Coin",
                date_range="211-208 BC",
                denomination=["denarius"],
                manufacturer=["Rome"],
                material=["silver"],
                authority=["Roman Republic"],
                geographic=["Rome"],
                images=[],
            )
        ]
    )
    agent = MagicMock()
    agent.run = AsyncMock(return_value=SimpleNamespace(output="comparison"))

    with (
        patch("app.services.chat.CatalogService", return_value=catalog),
        patch("app.services.chat._get_agent", return_value=agent),
    ):
        response = asyncio.run(service.chat(request))

    assert response.message == "comparison"
    catalog.find_coins_by_record_ids.assert_awaited_once_with(["rrc.1.1", "missing.id"])
    user_message = agent.run.await_args.args[0]
    assert "[Coin context:" in user_message
    assert "Test Coin (ID: rrc.1.1)" in user_message
    assert "Description: A test coin description" in user_message
    assert "Missing record IDs: missing.id" in user_message


def test_describe_image_validates_attachment_content_type_before_vision_call() -> None:
    agent = _create_agent(MOCK_LLM_MODEL)
    describe_image = agent._function_toolset.tools["describe_image"].function
    settings = _settings()
    vision = Vision(settings)
    describe = AsyncMock()
    request = ChatRequest(
        message="Identify this coin",
        attachment=ChatAttachment(filename="coin.gif", content_type="image/gif", data="Z2lmLWJ5dGVz"),
    )
    ctx = SimpleNamespace(
        deps=_Deps(config=settings, vision=vision, catalog=CatalogService(settings), request=request),
    )

    with patch.object(vision, "describe", new=describe):
        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(describe_image(ctx))  # type: ignore[arg-type]

    assert exc_info.value.status_code == 415
    describe.assert_not_called()


def test_describe_image_passes_decoded_supported_attachment_to_vision() -> None:
    agent = _create_agent(MOCK_LLM_MODEL)
    describe_image = agent._function_toolset.tools["describe_image"].function
    settings = _settings()
    vision = Vision(settings)
    describe = AsyncMock(return_value="Roman coin of Augustus")
    image_bytes = b"png-bytes"
    request = ChatRequest(
        message="Identify this coin",
        attachment=ChatAttachment(
            filename="coin.png",
            content_type="image/png",
            data=base64.b64encode(image_bytes).decode(),
        ),
    )
    ctx = SimpleNamespace(
        deps=_Deps(config=settings, vision=vision, catalog=CatalogService(settings), request=request),
    )

    with patch.object(vision, "describe", new=describe):
        result = asyncio.run(describe_image(ctx))  # type: ignore[arg-type]

    assert result == "Roman coin of Augustus"
    describe.assert_awaited_once_with(image_bytes, "image/png")
