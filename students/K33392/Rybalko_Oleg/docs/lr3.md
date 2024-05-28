# Лабораторная работа 3

# Задание
Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с базой данных и вызывать парсер через API и очередь.

# Решение

## REST API парсер

Создадим API для взаимодействия с парсером. Для этого создадим модель данных, которые мы будем ожидать от клиента
и добавим endpoint /parse. 

Данный endpoint принимает название парсера и получает транзакции. После этого мы возвращаем список из словарей.

```python
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from parsers import BtcComParser, BlockchainComParser
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


class ParserType(Enum):
    BTC_COM = "btccom"
    BLOCKHAIN_COM = "blockchaincom"

    def get_parser(self) -> BtcComParser | BlockchainComParser | None:
        if self.value == "btccom":
            return BtcComParser()
        if self.value == "blockchaincom":
            return BlockchainComParser()
        return None
        

class ParseRequest(BaseModel):
    parser: ParserType


@app.post("/parse")
async def parse(data: ParseRequest):
    if (parser := data.parser.get_parser()) is None:
        raise HTTPException(500, "invalid parser specified")
    return [i.model_dump() for i in await parser.aio_parse()]
```

## Backend для обращения к парсеру

Создадим endpoint, который будет обращаться к парсеру для получения транзакций.

```python
@router.post("")
async def parse(req: ParseRequest):
    async with aiohttp.ClientSession() as client:
        async with client.post("http://parser:8080/parse", json=dict(req)) as resp:
            return await resp.json()
```

После этого создадим endpoint'ы для синхронного и асинхронного создания задач в Celery.
Синхронный endpoint будет отправлять задачу в очередь и ожидать получения результата в течение 10 секунд.

Асинхронный endpoint создает задачу и возвращает список из идентификаторов.

GET запрос возвращает результат парсинга или 202 ACCEPTED статус код в том случае, когда задача находится в прогрессе

```python
@router.post("/celery/sync")
def parse_celery_sync(req: ParseRequest):
    result = app.send_task("tasks.parse", args=[req.parser])
    return result.get(timeout=10)

@router.post("/celery/async")
def parse_async(req: ParseRequest):
    task = app.send_task("tasks.parse", args=[req.parser])
    return task.as_list()

@router.get("/celery/task")
def get_task_result(task_id: str):
    result = AsyncResult(task_id, app=app)
    if not result.ready():
        return Response(HTTPStatus.ACCEPTED)
    return result.get()
```


## Dockerfile для backend

Упакуем backend код в докер-образ.
Для этого нам необходимо создать Dockerfile.


```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN mount=type=cache,target=/root/.cache pip3 install -r requirements.txt
COPY . .

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Данный докерфайл копирует все файлы из рабочей директории в образ, устанавливает необходимые зависимости и запускает сервер.

## Dockerfile для парсера

Для парсера создадим два докерфайла – один для запуска REST API, другой для Celery.
Dockefile для REST такой же, как и для backend, а для Celery нам необходимо изменить ENTRYPOINT для запуска воркера.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN mount=type=cache,target=/root/.cache pip3 install -r requirements.txt
COPY . .

ENTRYPOINT [ "celery", "-A", "tasks", "worker", "--loglevel=INFO"]
```

## docker-compose.yaml

backend будет собираться из директории lr1. Для этого укажем context.
Более того, установим переменные окружения для взаимодействия с POSTGRES и CELERY.
Данный сервис должен запускаться после redis, db и парсера.
```docker-compose
version: '3.9'

services:
  backend:
    build:
      context: ./lr1
    ports:
      - "8080:8080"
    environment:
      - DB_URL=postgresql://postgres:password@db:5432/postgres
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - db
      - redis
      - parser
```

Парсер должен собираться из директории lr2/ex2 и докерфайла Dockefile.celery.
Данный сервис зависит от db и redis.

```docker-compose

  parser:
    build:
      context: ./lr2/ex2
      dockerfile: Dockerfile.celery
    environment:
      - DB_URL=postgresql://postgres:password@db:5432/postgres
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - db
      - redis
```

Поднимем две базы данных – redis и postgresql. redis необходим для хранения задач Celery, а postgresql для backend.

```docker-compose
  redis:
    image: 'bitnami/redis:latest'
    environment:
      - ALLOW_EMPTY_PASSWORD=yes

  db:
    image: postgres
    container_name: postgres_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=postgres

volumes:
  postgres_data:

```


