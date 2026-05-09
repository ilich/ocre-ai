import asyncio
import json
from pathlib import Path
from typing import Any

import typer
from beanie import init_beanie
from dotenv import load_dotenv
from pydantic_ai import Embedder
from pymongo import AsyncMongoClient

from app.core.settings import get_settings
from app.models.domain import Coin, Geographic, Metadata, MetadataType

load_dotenv()
cli = typer.Typer()


@cli.callback()
def main() -> None:
    """OCRE AI management CLI."""


def _coin_to_text(coin: Coin) -> str:
    text = ["#" + coin.title + "\n"]
    if coin.description:
        text.append(coin.description + "\n")
    if coin.from_year and coin.to_year:
        text.append(f"Date range: {coin.from_year} - {coin.to_year}")
    elif coin.from_year:
        text.append(f"From year: {coin.from_year}")
    elif coin.to_year:
        text.append(f"To year: {coin.to_year}")
    if coin.denomination:
        text.append("Denomination: " + ", ".join(coin.denomination))
    if coin.manufacturer:
        text.append("Manufacturer: " + ", ".join(coin.manufacturer))
    if coin.material:
        text.append("Material: " + ", ".join(coin.material))
    if coin.authority:
        text.append("Authority: " + ", ".join(coin.authority))
    if coin.geographic:
        text.append(
            "Geographic: " + ", ".join(f"{g.name} ({g.type})" for g in coin.geographic if isinstance(g, Geographic))
        )
    return "\n".join(text)


async def _seed(dataset: Path) -> None:
    config = get_settings()
    client: AsyncMongoClient[Any] = AsyncMongoClient(config.mongodb_uri)
    try:
        db = client.get_database(config.mongodb_database)

        typer.echo("Dropping collections...")
        await db["geographics"].drop()
        await db["coins"].drop()
        await db["metadata"].drop()

        await init_beanie(database=db, document_models=[Geographic, Coin, Metadata])

        records: list[dict[str, Any]] = json.loads(dataset.read_text())
        typer.echo(f"Loaded {len(records)} records from {dataset}")

        # --- Geographic lookup ---
        typer.echo("Seeding geographics...")
        geo_map: dict[tuple[str, str], Geographic] = {}
        for record in records:
            for g in record.get("geographic", []):
                key = (g["name"], g["type"])
                if key not in geo_map:
                    geo = Geographic(name=g["name"], type=g["type"])
                    await geo.insert()
                    geo_map[key] = geo
        typer.echo(f"  {len(geo_map)} unique geographics inserted")

        # --- Metadata ---
        typer.echo("Seeding metadata...")
        meta_values: dict[MetadataType, set[str]] = {t: set() for t in MetadataType}
        for record in records:
            if obj_type := record.get("object_type"):
                meta_values[MetadataType.OBJECT_TYPE].add(obj_type)
            for val in record.get("denomination", []):
                if val is not None:
                    meta_values[MetadataType.DENOMINATION].add(val)
            for val in record.get("manufacturer", []):
                if val is not None:
                    meta_values[MetadataType.MANUFACTURER].add(val)
            for val in record.get("material", []):
                if val is not None:
                    meta_values[MetadataType.MATERIAL].add(val)
            for val in record.get("authority", []):
                if val is not None:
                    meta_values[MetadataType.AUTHORITY].add(val)

        metadata_docs = [
            Metadata(type=meta_type, value=value)
            for meta_type, values in meta_values.items()
            for value in sorted(values)
        ]
        await Metadata.insert_many(metadata_docs)
        typer.echo(f"  {len(metadata_docs)} metadata entries inserted")

        # --- Coins ---
        typer.echo("Seeding coins...")
        coins = [
            Coin(
                record_id=record["record_id"],
                title=record["title"],
                description=record["description"],
                object_type=record["object_type"],
                from_year=record.get("from_year"),
                to_year=record.get("to_year"),
                date_range=record.get("data_range"),
                denomination=[v for v in record.get("denomination", []) if v is not None],
                manufacturer=[v for v in record.get("manufacturer", []) if v is not None],
                material=[v for v in record.get("material", []) if v is not None],
                authority=[v for v in record.get("authority", []) if v is not None],
                geographic=[
                    geo_map[(g["name"], g["type"])]
                    for g in record.get("geographic", [])
                    if (g["name"], g["type"]) in geo_map
                ],
                images=record.get("images", []),
            )
            for record in records
        ]
        await Coin.insert_many(coins)
        typer.echo(f"  {len(coins)} coins inserted")

        typer.echo("Done.")
    finally:
        await client.close()


async def _embed_coins() -> None:
    config = get_settings()
    client: AsyncMongoClient[Any] = AsyncMongoClient(config.mongodb_uri)
    try:
        db = client.get_database(config.mongodb_database)
        await init_beanie(database=db, document_models=[Geographic, Coin, Metadata])

        coins = await Coin.find(Coin.embedding == None, fetch_links=True).to_list()  # noqa: E711
        typer.echo(f"Found {len(coins)} coins without embeddings")

        if not coins:
            return

        embedder = Embedder(config.ai_embedding_model)
        for i, coin in enumerate(coins, start=1):
            typer.echo(f"  [{i}/{len(coins)}] {coin.title}")
            result = await embedder.embed(_coin_to_text(coin), input_type="document")
            coin.embedding = list(result.embeddings[0])
            await coin.save()

        typer.echo(f"Done. Updated {len(coins)} coins.")
    finally:
        await client.close()


@cli.command()
def seed(
    dataset: Path = typer.Argument(..., help="Path to the OCRE JSON dataset"),
) -> None:
    """Drop and re-seed the Geographic, Metadata, and Coin collections."""
    asyncio.run(_seed(dataset))


@cli.command()
def embed_coins() -> None:
    """Compute and store embeddings for all coins that do not have one yet."""
    asyncio.run(_embed_coins())


if __name__ == "__main__":
    cli()
