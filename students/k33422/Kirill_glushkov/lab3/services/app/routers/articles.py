from fastapi import APIRouter, Depends, HTTPException
import aiohttp
import ssl

from sqlmodel import Session, select
from ..core import db
from ..core.config import settings
from ..models.articles import ArticlesParseResponse, URLData
from starlette import status

from services.parser.database import Article

router = APIRouter()


@router.get("/parse-status/{task_id}")
async def get_status(task_id: str):
    parser_url = settings.PARSER_URL + "/status/" + task_id

    async with aiohttp.ClientSession() as session:
        async with session.get(parser_url) as response:
            if response.status != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status, detail="Error fetching task status"
                )
            data = await response.json()
            return data


@router.get("/")
async def get_articles(
    session: Session = Depends(db.get_session),
):
    articles = session.exec(select(Article)).all()
    return articles


@router.post("/fetch-article-title")
async def fetch__article_title(data: URLData):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        async with session.post(
            settings.PARSER_URL + "/get-article-title/", json={"url": str(data.url)}
        ) as response:
            if response.status != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status,
                    detail="Error fetching the title from parser",
                )
            data = await response.json()
            task_id = data.get("task_id")

            return ArticlesParseResponse(ok=True, task_id=task_id)
