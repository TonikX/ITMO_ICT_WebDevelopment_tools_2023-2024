import uvicorn
from fastapi import FastAPI
from src.web_api.config import db
from src.web_api.routes.main import api_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    db.init_db()


app.include_router(api_router, prefix="/api")


def start():
    uvicorn.run("src.web_api.main:app", host="0.0.0.0", port=8000, reload=True)
