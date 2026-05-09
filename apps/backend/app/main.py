from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from asgi_correlation_id import CorrelationIdMiddleware
from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import AsyncMongoClient

from app.core.logging import setup_logging
from app.core.settings import get_settings
from app.models.domain import Coin, Geographic, Metadata, User
from app.routes import auth, catalog, health, user

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging()
    config = get_settings()
    client: AsyncMongoClient[Any] = AsyncMongoClient(config.mongodb_uri)
    await init_beanie(
        database=client.get_database(config.mongodb_database), document_models=[User, Geographic, Coin, Metadata]
    )
    yield
    await client.close()


config = get_settings()
app = FastAPI(title="OCRE AI Backend", lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=config.cors_origins.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
