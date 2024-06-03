import json
from celery import Celery
import aiohttp
from bs4 import BeautifulSoup
from .database import add_article_to_database
import asyncio
from pydantic import BaseModel
from starlette import status
from .config import settings


class TaskResponse(BaseModel):
    status: str
    data: str


celery_app = Celery(
    "parser",
    broker=f"{settings.REDIS_URL}/0",
    backend=f"{settings.REDIS_URL}/0",
)

celery_app.conf.update(
    task_routes={
        "tasks.parse_article": "main-queue",
    },
)


async def fetch_title(url: str) -> TaskResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != status.HTTP_200_OK:
                return TaskResponse(status="error", data="Could not fetch given URL")
            html = await response.text()
            parsed_html = BeautifulSoup(html, "html.parser")
            title = parsed_html.title.string
            add_article_to_database("celery", url, title)
            return json.loads(
                TaskResponse(status="success", data=title).model_dump_json()
            )


@celery_app.task
def parse_article(url: str) -> TaskResponse:
    return asyncio.get_event_loop().run_until_complete(fetch_title(url))


if __name__ == "__main__":
    celery_app.start()
