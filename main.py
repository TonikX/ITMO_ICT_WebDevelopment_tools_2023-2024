from fastapi import FastAPI, HTTPException, Depends, APIRouter
from typing import List
from sqlmodel import Session, select

from connection import init_db, get_session
from endpoints import task, user, auth, category, tag
from models import Task, Category, Tag, TaskDefault, TagDefault, CategoryDefault

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


api_router = APIRouter()
api_router.include_router(task.router, prefix="/task", tags=["task"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(tag.router, prefix="/tag", tags=["tag"])
api_router.include_router(user.router, prefix="/user", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

app.include_router(api_router)