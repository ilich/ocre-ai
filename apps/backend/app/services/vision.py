from typing import Annotated, Literal

from fastapi import Depends
from pydantic_ai import Agent, BinaryContent

from app.core.settings import Settings, get_settings

SupportedImageContentType = Literal["image/png", "image/jpeg"]


class Vision:
    def __init__(self, config: Settings) -> None:
        self.config = config

    async def describe(self, image: bytes, content_type: SupportedImageContentType) -> str:
        prompt = """
You are an expert Roman numismatist.

Analyze the uploaded image.

If the image is NOT a Roman coin or ancient numismatic object, return an empty string and nothing else.

If the image is a Roman coin, return a concise plain-text description optimized for semantic/vector search.

Requirements:
- Keep the response concise and information-dense.
- Do NOT return JSON or markdown.
- Extract and include ALL visible text exactly as seen.
- Mention uncertain letters with ? or [ ].
- Include:
  - ruler/emperor name
  - denomination if identifiable
  - approximate date
  - mint if identifiable
  - obverse imagery
  - reverse imagery
  - important symbols/deities/objects
  - Latin inscriptions
  - English meaning of inscriptions
  - historical keywords
  - authenticity observations if notable

Output format:

Roman coin of [ruler], [date], [denomination], minted in [mint if known]. Obverse: [concise description]. Legend: “[exact text]”. Reverse: [concise description]. Legend: “[exact text]”. Translation: [short translation]. Keywords: [important searchable terms]. Authenticity notes: [short note].

Rules:
- Prioritize searchable numismatic terminology.
- Avoid filler words.
- Do not speculate aggressively.
- If uncertain, explicitly say “possibly” or “unclear”.
- Maximum 120 words.
- If the image is generic, modern, unrelated, or not clearly a Roman/ancient coin, return an empty string.
"""
        agent = Agent(self.config.ai_model)
        result = await agent.run(
            [
                prompt,
                BinaryContent(data=image, media_type=content_type, identifier="coin_image"),
            ]
        )

        return result.output


def get_vision(config: Annotated[Settings, Depends(get_settings)]) -> Vision:
    return Vision(config)
