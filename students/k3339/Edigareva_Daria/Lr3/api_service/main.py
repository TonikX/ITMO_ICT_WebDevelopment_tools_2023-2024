from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: D401
    # Здесь можно подключить мониторинг / логи, но пока просто yield
    yield


app = FastAPI(title="API Service", version="1.0.0", lifespan=lifespan)
app.include_router(router)