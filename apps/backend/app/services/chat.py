import base64
from typing import Annotated

from fastapi import Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart

from app.core.settings import Settings, get_settings
from app.models.catalog import FilterParams
from app.models.chat import ChatHistoryItem, ChatRequest, ChatResponse
from app.services.catalog import CatalogService
from app.services.vision import SupportedImageContentType, Vision

SUPPORTED_ATTACHMENT_IMAGE_TYPES: dict[str, SupportedImageContentType] = {
    "image/png": "image/png",
    "image/jpeg": "image/jpeg",
}


class _Deps(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: Settings
    vision: Vision
    catalog: CatalogService
    request: ChatRequest


_SYSTEM_PROMPT = """
You are an expert in Roman History, Archaeology, and Numismatics, specializing in Hellenistic, Greek, Roman, and Byzantine coins, artifacts, and history.

Decision flow — follow exactly in order:

1. If an image was attached (the user message starts with [Attached image:]), call `describe_image` first to analyze it. Use the returned description to formulate a search query and call `search_coins`.
2. If the user's message contains ambiguous pronouns (it, this, that, they, them, these, those, he, she, his, her) AND there is prior conversation history, call `rewrite_question` to produce a clear, pronoun-free version before proceeding.
3. If the question asks about finding, listing, or identifying specific coins in the database, call `search_coins` with a descriptive query and present the results in a human-readable format.
4. If the question is about Hellenistic, Greek, Roman, or Byzantine history, archaeology, or numismatics (rulers, dates, events, artifacts, coin types, minting, inscriptions, etc.), answer directly from your expertise.
5. For any other topic, respond exactly: "I am a Roman historical expert system specializing in ancient numismatics and Greco-Roman history. I cannot help with this type of question."
"""


def _build_message_history(history: list[ChatHistoryItem]) -> list[ModelMessage]:
    messages: list[ModelMessage] = []
    for item in history:
        if item.role == "user":
            messages.append(ModelRequest(parts=[UserPromptPart(content=item.content)]))
        else:
            messages.append(ModelResponse(parts=[TextPart(content=item.content)], model_name=None))
    return messages


_main_agent: Agent[_Deps, str] | None = None


def _validated_attachment_content_type(content_type: str) -> SupportedImageContentType:
    supported_content_type = SUPPORTED_ATTACHMENT_IMAGE_TYPES.get(content_type)
    if supported_content_type:
        return supported_content_type

    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="Only PNG and JPG images are supported",
    )


def _create_agent(model: str) -> Agent[_Deps, str]:
    agent: Agent[_Deps, str] = Agent(
        model,
        deps_type=_Deps,
        output_type=str,
        system_prompt=_SYSTEM_PROMPT,
    )

    @agent.tool
    async def describe_image(ctx: RunContext[_Deps]) -> str:
        """Analyze the image attached to the current request. Returns a numismatic description for searching."""
        logger.info("Tool called: describe_image")
        attachment = ctx.deps.request.attachment
        if not attachment:
            return "No image was attached."
        content_type = _validated_attachment_content_type(attachment.content_type)
        image_bytes = base64.b64decode(attachment.data)
        description = await ctx.deps.vision.describe(image_bytes, content_type)
        return description if description else "The image does not appear to be a Roman or ancient coin."

    @agent.tool
    async def rewrite_question(ctx: RunContext[_Deps], question: str) -> str:
        """Rewrite the question to replace ambiguous pronouns with explicit noun phrases from conversation history.

        Args:
            question: The original question containing pronouns to resolve.
        """
        logger.info("Tool called: rewrite_question | question={!r}", question)
        history = ctx.deps.request.history or []
        if not history:
            return question
        history_text = "\n".join(f"{item.role.upper()}: {item.content}" for item in history)
        rewriter: Agent[None, str] = Agent(
            ctx.deps.config.ai_model,
            output_type=str,
            system_prompt=(
                "You rewrite questions to eliminate ambiguous pronouns by substituting them with "
                "the explicit nouns they refer to, based on the provided conversation history. "
                "Return only the rewritten question, nothing else."
            ),
        )
        result = await rewriter.run(f"Conversation history:\n{history_text}\n\nQuestion to rewrite: {question}")
        return result.output

    @agent.tool
    async def search_coins(ctx: RunContext[_Deps], query: str) -> str:
        """Search the coin database for coins matching the query and return formatted results.

        Args:
            query: A descriptive search query (e.g. 'denarius of Nero from Rome').
        """
        logger.info("Tool called: search_coins | query={!r}", query)
        params = FilterParams(search=query, limit=10)
        result = await ctx.deps.catalog.find_coins(params)

        if not result.items:
            return f"No coins found in the database matching '{query}'."

        lines = [f"Found {result.total} coin(s) matching '{query}'. Showing top {len(result.items)}:\n"]
        for coin in result.items:
            entry: list[str] = [f"• {coin.title} (ID: {coin.id})"]
            if coin.date_range:
                entry.append(f"  Date: {coin.date_range}")
            if coin.authority:
                entry.append(f"  Authority: {', '.join(coin.authority)}")
            if coin.denomination:
                entry.append(f"  Denomination: {', '.join(coin.denomination)}")
            if coin.material:
                entry.append(f"  Material: {', '.join(coin.material)}")
            if coin.manufacturer:
                entry.append(f"  Mint: {', '.join(coin.manufacturer)}")
            if coin.geographic:
                entry.append(f"  Geography: {', '.join(coin.geographic)}")
            if coin.description:
                preview = coin.description[:200].rstrip()
                entry.append(f"  Description: {preview}{'...' if len(coin.description) > 200 else ''}")
            lines.append("\n".join(entry))

        return "\n\n".join(lines)

    return agent


def _get_agent(model: str) -> Agent[_Deps, str]:
    global _main_agent
    if _main_agent is None:
        _main_agent = _create_agent(model)
    return _main_agent


class ChatService:
    def __init__(self, config: Settings) -> None:
        self.config = config

    async def chat(self, request: ChatRequest) -> ChatResponse:
        deps = _Deps(
            config=self.config,
            vision=Vision(self.config),
            catalog=CatalogService(self.config),
            request=request,
        )

        user_message = request.message
        if request.attachment:
            _validated_attachment_content_type(request.attachment.content_type)
            user_message = f"[Attached image: {request.attachment.filename}]\n{user_message}"
        if request.coins_context:
            coins_list = ", ".join(request.coins_context)
            user_message = f"{user_message}\n\n[Coin context: {coins_list}]"

        agent = _get_agent(self.config.ai_model)
        message_history = _build_message_history(request.history or [])

        result = await agent.run(
            user_message,
            deps=deps,
            message_history=message_history,
        )
        return ChatResponse(message=result.output)


def get_chat_service(config: Annotated[Settings, Depends(get_settings)]) -> ChatService:
    return ChatService(config)
