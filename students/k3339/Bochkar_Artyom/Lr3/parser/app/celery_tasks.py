import asyncio
from celery import Celery
from app.parser_service import parse_and_save_books

celery_app = Celery(
    'bookcrossing',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
)


@celery_app.task
def parse_url_task(url: str):
    result = asyncio.run(parse_and_save_books(url))
    return f"There are {result} newly parsed Books"