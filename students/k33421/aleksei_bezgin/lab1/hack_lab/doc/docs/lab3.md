# Docker. Упаковка FastAPI приложения в Docker, Работа с источниками данных и Очереди

1. Первым делом напишем Dockerfile для нашего FastAPI приложения, тем самым создав его образ для дальнейшего использования в Docker-compose:
```commandline
FROM python:3.11.6-slim-bookworm as base

WORKDIR /app
COPY requirements.txt /app/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

FROM base as installer

RUN apt update && apt install --no-install-recommends -y build-essential libpq-dev
RUN pip install uv
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV=/opt/venv
RUN uv pip install --no-cache -r requirements.txt

FROM base as runtime

RUN apt update && \
    apt install --no-install-recommends -y libpq-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=installer /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./src/ .
```

В первом блоке мы устанавливаем рабочую директорию app/, копируем requirements.txt и устанавливаем значения переменных окружения
После этого указываем необходимые для компилирования библиотек пакеты, ставим пакетный менеджер uv, создаем виртуальное окружение и устанавливаем туда зависимости из requirements.txt
Наконец, устанавливаем пакеты для работы с БД, копируем venv и файлы из директории с приложением

2. Теперь создаем первую версию docker-compose.yml, в который поместим стандартный postgres контейнер для БД и контейнер на образе нашего приложения:
```commandline
version: "3.4"

services:
  db:
    image: postgres:14.1
    hostname: ${DB_HOST}
    container_name: db
    restart: always
    volumes:
      - ./db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    env_file:
      - .env
 
  rest:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: rest
    command: python -m uvicorn main:app --host 0.0.0.0 --port 8081
    restart: always
    volumes:
      - ./src/:/app
    ports:
      - "8081:8081"
    env_file:
      - .env
    depends_on:
      - db
```

Теперь наше приложение способно работать так же, как и раньше, но с помощью Docker

3. Теперь интегрируем парсер

Сначала добавим в docker-compose новые контейнеры: Redis для сохранения результатов выполнения задач и RabbitMQ для брокинга сообщений с Celery:
```commandline
  rabbitmq:
    image: rabbitmq:3.13.1
    hostname: ${RABBITMQ__HOST}
    container_name: rabbitmq
    restart: always

  redis:
    image: redis:7.2.4
    hostname: ${REDIS__HOST}
    container_name: redis
    restart: always
```

В директории с приложением создадим директорию для Celery и создадим там модуль для подключения Celery и задачи для парсинга:
```commandline
import datetime

import requests
from bs4 import BeautifulSoup
from celery import Celery
from sqlmodel import Session

from config import settings
from db.connection import engine
from db.models import Hackathon, Task

app = Celery(
    "celery_app",
    result_backend=f"redis://{settings.redis_host}:{settings.redis_port}/0",
    broker=f"pyamqp://guest@{settings.rabbitmq_host}:{settings.rabbitmq_port}//",
)


@app.task
def parse_hackathon(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    hack_name = soup.find("h1").text
    paragraphs = list(map(lambda x: x.text, soup.find_all('p')))
    hack_case = '\n'.join(paragraphs)
    case_title = paragraphs[0]

    with Session(engine) as session:
        hackathon = Hackathon(
            name=hack_name,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        session.add(hackathon)
        session.commit()
        session.refresh(hackathon)

        task = Task(
            title=case_title,
            description=hack_case,
            requirements="Be cool",
            evaluation_criteria="Accuracy",
            hackathon_id=hackathon.id
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        print(hackathon.name)

        return {"hackathon": hackathon.model_dump(), "task": task.model_dump()}
```

Теперь добавим контейнер для Celery:
```commandline
  celery:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: celery
    command: python -m celery -A celery_worker.app worker
    restart: always
    volumes:
      - ./src/:/app
    env_file:
      - .env
    depends_on:
      - rest
      - redis
      - rabbitmq
```

4. Наконец, добавим новые эндпоинты в приложение:
```commandline
from fastapi import APIRouter
from celery import current_app as celery_app

from celery_worker.app import parse_hackathon
from rest.celery_tasks.schemas import TaskIdResponse, TaskStatusResponse, ParsedDataResponse

router = APIRouter()


@router.post("/start_parsing")
async def start_parsing(url: str) -> TaskIdResponse:
    task = parse_hackathon.delay(url)
    return TaskIdResponse.model_validate({"task_id": task.id})


@router.get("/check_parsing")
async def check_parsing(task_id: str) -> TaskStatusResponse:
    task = celery_app.AsyncResult(task_id)
    status = task.status

    return TaskStatusResponse.model_validate({"status": status})


@router.get("/get_parsing")
async def get_parsing(task_id: str) -> ParsedDataResponse:
    task = celery_app.AsyncResult(task_id)
    result = task.result

    data = result
    print(data)

    return ParsedDataResponse.model_validate({"data": data})
```

В данном случае api/v1/celery/start_parsing позволяет запустить парсинг данных о хакатоне по url
В api/v1/celery/check_parsing по task_id можно проверить готовность парсинга
В api/v1/celery/get_parsing по task_id можно получить итоговый результат (словарь с дампами моделей Hackaton и Task)

Можно так же использовать исходные get-методы для проверки того, что данные действительно сохранились в БД

Итоговый docker-compose.yml:
```commandline
version: "3.4"

services:
  db:
    image: postgres:14.1
    hostname: ${DB_HOST}
    container_name: db
    restart: always
    volumes:
      - ./db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    env_file:
      - .env

  rabbitmq:
    image: rabbitmq:3.13.1
    hostname: ${RABBITMQ__HOST}
    container_name: rabbitmq
    restart: always

  redis:
    image: redis:7.2.4
    hostname: ${REDIS__HOST}
    container_name: redis
    restart: always

  rest:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: rest
    command: python -m uvicorn main:app --host 0.0.0.0 --port 8081
    restart: always
    volumes:
      - ./src/:/app
    ports:
      - "8081:8081"
    env_file:
      - .env
    depends_on:
      - db

  celery:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: celery
    command: python -m celery -A celery_worker.app worker
    restart: always
    volumes:
      - ./src/:/app
    env_file:
      - .env
    depends_on:
      - rest
      - redis
      - rabbitmq
```