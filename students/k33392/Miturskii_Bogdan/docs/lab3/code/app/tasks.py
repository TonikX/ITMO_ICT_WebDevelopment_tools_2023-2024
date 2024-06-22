from celery import Celery
import asyncio
from app.parser import main as async_parser

celery_app = Celery(__name__, broker="redis://redis:6379/0", backend="redis://redis:6379/0")

@celery_app.task(name="app.tasks.parse_urls_async")
def parse_urls_async(urls: list[str]):
    result = asyncio.run(async_parser(urls))
    return result
