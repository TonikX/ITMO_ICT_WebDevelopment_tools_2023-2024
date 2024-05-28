import aiohttp
import fastapi
from fastapi import APIRouter
from fastapi import Depends

from src.adapters.db import SqlalchemyWorker
from src.settings.connection import get_session
from src.repos.parser import parse_and_save


parse_router = APIRouter(prefix="", tags=["parser"])


@parse_router.post("/parse")
async def parse(url: str, session=Depends(get_session)):
    sqlalchemy_worker = SqlalchemyWorker(session)
    try:
        async with aiohttp.ClientSession() as request_session:
            response = await request_session.get(url)  #парсер запрашивает html
            response.raise_for_status()
            html = await response.text()
            parse_and_save(url, html, sqlalchemy_worker)
            #parse_url_content.delay(url, html, sqlalchemy_worker) # вызов задачи
            return {"message": "Parsing is started"}
    except aiohttp.client.ClientConnectorError as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))
