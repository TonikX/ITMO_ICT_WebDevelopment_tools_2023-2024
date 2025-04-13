from fastapi import FastAPI
from connection import init_db

from app.api import app_router
from users.api import user_router


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(user_router)
app.include_router(app_router)