from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.parser_service import parse_and_save
from db.connection import init_db
from db.parse import ParseRequest

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

@app.post("/parse")
async def parse_url(parse_request: ParseRequest):
    print(f"Parsing URL: {parse_request.url}")
    await parse_and_save(parse_request.url)
    return {"message": "Parsing completed"}