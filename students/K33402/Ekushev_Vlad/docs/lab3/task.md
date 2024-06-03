# Ход работы

Для начала нужно было инициализировать общее приложение с двумя лабораторными (1 и 2) – `poetry init`

Сервисы я поместил в папку `services`, тем самым у меня получилась такой монорепозиторий с общими зависимостями в корне проекта.

# Celery

Нужно объявить таску для Celery через декоратор `@Celery.task()`

```Python title="celery_app.py"
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
```

# FastAPI

Добавил новый роутер `articles` в приложение из первой лабораторной. Нужен он для удобного вывода результатов сервиса.

```Python title="articles.py"
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
```

# Docker

Сложная структура докерфайла из-за того, что в проекте используется `poetry`, поэтому его нужно сначала установить, а потом использовать.

```Dockerfile title="Dockerfile"
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.8.2 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"


ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR /app
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential libpq-dev
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev
COPY . .
```

В композ-файле объявлены пять сервисов:

- База данных (db)
- Redis (redis)
- Приложение API (app)
- Celery воркер (celery_app)
- FastAPI парсера (parser)

```YML title="docker-compose.yml"
services:
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=itmo-web-lab3
    volumes:
      - ./postgres:/var/lib/postgresql/data
    expose:
      - 5432
    restart: always

  app:
    build:
      context: .
      dockerfile: Dockerfile
    tty: true
    env_file:
      - .env
    ports:
      - 8000:8000
    depends_on:
      - db
    command: poetry run python -m uvicorn services.app.main:app --host 0.0.0.0 --port 8000
    healthcheck:
      test: ['CMD', 'pg_isready']
      interval: 10s
      timeout: 5s
      retries: 5

  parser:
    build:
      context: .
      dockerfile: Dockerfile
    tty: true
    env_file:
      - .env
    ports:
      - 9000:9000
    depends_on:
      - db
    command: poetry run python -m uvicorn services.parser.main:app --host 0.0.0.0 --port 9000
    healthcheck:
      test: ['CMD', 'pg_isready']
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis
    expose:
      - 6379
    restart: always

  celery_app:
    build:
      context: .
      dockerfile: Dockerfile
    command: poetry run celery -A services.parser.celery_app worker --loglevel=info
    restart: always
    env_file:
      - .env
    depends_on:
      - redis
      - app
```
