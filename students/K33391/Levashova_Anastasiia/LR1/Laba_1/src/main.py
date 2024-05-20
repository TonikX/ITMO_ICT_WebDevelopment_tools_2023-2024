from fastapi import FastAPI

from connection import init_db
from fastapi import APIRouter
from api import label, category, task, user, auth

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


api_router = APIRouter()
api_router.include_router(task.router, prefix="/task", tags=["task"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(label.router, prefix="/label", tags=["label"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])


app.include_router(api_router, prefix="/api")
