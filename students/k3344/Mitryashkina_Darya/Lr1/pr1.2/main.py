from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import select
from connection import init_db, close_db
from contextlib import asynccontextmanager
from typing_extensions import TypedDict
from connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from category_router import router as category_router
from users_router import router as user_router
from task_router import router as task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(category_router, prefix="/categories", tags=["Categories"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def hello():
    return "Hello!"
