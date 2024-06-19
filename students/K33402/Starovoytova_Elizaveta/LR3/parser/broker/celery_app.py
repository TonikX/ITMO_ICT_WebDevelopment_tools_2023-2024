import os

from celery import Celery
from dotenv import load_dotenv

from database.save_data import save_author_and_books_from_json
from parser.parser import parse_author_info

# Загрузка переменных окружения из .env файла
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")


celery_app = Celery(
    "parser",
    broker=f"{REDIS_URL}/0",
    backend=f"{REDIS_URL}/0",
)

celery_app.conf.update(
    task_routes={
        "tasks.parse_books": "main-queue",
    },
)


@celery_app.task
def parse_books(url: str):
    author_info = parse_author_info(url)
    save_author_and_books_from_json(author_info)
    return {"message": "Parsing completed"}
