from contextlib import asynccontextmanager
from typing import AsyncGenerator

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from app.core.logging import setup_logging
from app.routes import health


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging()
    yield


app = FastAPI(title="OCRE AI Backend", lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(health.router, prefix="/health", tags=["health"])
