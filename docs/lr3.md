# ЛР №3

В данной лаборатонрой работе необходимо было упаковать приложение FastpApi и парсер информации с помощью Docker.


## Dockerfile
Для начала, были описаны докер файлы для FastApi и Парсера.

FastApi:

```python
FROM python:3.12

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
```

Парсер:

```python

FROM python:3.12

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

```

## Docker-compose

После чего был описан файл docker-compose:

```python
services:
  lr1:
    container_name: lr1
    build: ./../ЛР1/ЛР
    depends_on:
      - db
    ports:
      - 3000:3000
    restart: always
    env_file:
      - ./../ЛР1/ЛР/.env
      
  lr3:
    container_name: lr3
    build: .
    depends_on:
      - db
    ports:
      - 3001:3001
    restart: always
    env_file:
      - .env
      
  db:
    container_name: postgres
    image: postgres
    environment:
      - POSTGRES_DB=lr1
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=1
    ports:
      - 5432:5432
    restart: always
    
  redis:
    image: redis:7
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    command: celery -A celeryTask worker --loglevel=info
    depends_on:
      - redis
      - db

  flower:
    build:
      context: .
    container_name: flower_app
    command: celery -A celeryTask flower
    depends_on:
      - redis
      - celery_worker
    ports:
      - 5555:5555
```

В данном файле мы подключили наши приложения, а также другие приложения для работы с ними.

## Celery
В данном проекте Celery выполняет асинхроную работу по работе парсера, очередью задач для него является redis.

Celery:

```python
from celery import Celery
from celery.utils.log import get_task_logger
from asynctask import main
import asyncio

logger = get_task_logger(__name__)

celery = Celery('worker', broker='redis://redis:6379')

@celery.task
def parse_and_save(urls):
    logger.info(f"Started task with URLs: {urls}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))
    logger.info(f"Completed task with URLs: {urls}")
```

## Выполнение задачи при помощи Celery

Создаём end-point, где будем вызывать наш celery:

```python
@app.get("/celery")
def test(url: str):
    urls = [url]
    results = parse_and_save_celery.apply_async(args=[urls])
    return {"message": "Parsing started"}
```

После вызова задачи она поместится в очередь и выполнится, статус задач можно посмотреть с помощью flower, перейдя на localhost:5555/tasks