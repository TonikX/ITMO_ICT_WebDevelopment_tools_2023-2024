from typing import Any, AsyncGenerator
import uvicorn
from fastapi import FastAPI
from app.core import db
from app.core.config import settings
from app.routers import api_router
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    db.init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


def start() -> None:
    uvicorn.run("app.main:app", host=settings.DOMAIN, port=settings.PORT, reload=True)
