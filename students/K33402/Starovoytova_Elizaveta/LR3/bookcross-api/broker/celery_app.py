import os

from celery import Celery
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")


celery_app = Celery(
    "parser",
    broker=f"{REDIS_URL}/0",
    backend=f"{REDIS_URL}/0",
)
