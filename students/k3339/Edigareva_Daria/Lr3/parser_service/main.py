from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI

from redis_listener import start_listener
from routes import router

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: D401
    """Создаём Redis‑клиент и запускаем listener во время жизни приложения."""
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    listener_task = asyncio.create_task(start_listener(redis))
    try:
        yield  # приложение запущено
    finally:
        listener_task.cancel()
        try:
            await listener_task
        except asyncio.CancelledError:
            pass
        await redis.close()


app = FastAPI(title="Parser Service", version="1.0.0", lifespan=lifespan)
app.include_router(router)