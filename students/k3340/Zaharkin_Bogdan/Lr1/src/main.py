from fastapi import FastAPI

from src.db.connection import init_db
from src.api.routes import router

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()
