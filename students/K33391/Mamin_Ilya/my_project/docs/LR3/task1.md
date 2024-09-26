# Упаковка FastAPI приложения, базы данных и парсера данных в Docker

Создание FastAPI приложения: Создано в рамках лабораторной работы номер 1

Создание базы данных: Создано в рамках лабораторной работы номер 1

Создание парсера данных: Создано в рамках лабораторной работы номер 2

## Реализация парсера

Реализуйте возможность вызова парсера по http Для этого можно сделать отдельное приложение FastAPI для парсера или воспользоваться библиотекой socket или подобными.

```python
from fastapi import FastAPI, BackgroundTasks
from parse import parse_and_save
from database import get_session
from fastapi import Depends, status
from schemas import Parce

app = FastAPI()


@app.post("/parse/")
async def parse(
    url: str, background_tasks: BackgroundTasks, session=Depends(get_session)
):
    background_tasks.add_task(parse_and_save, url, session)
    return {"message": "Parse started."}


@app.get("/get-tasks/")
def cases_list(session=Depends(get_session)) -> list[Parce]:
    return session.query(Parce).all()
```

## Создание Dockerfile

Чтобы обеспечить функционирование приложения, требуется развернуть три контейнера: контейнер для базы данных, контейнер для парсера и контейнер для FastAPI-приложения. Для их создания мы использовали два Dockerfile, при этом для образа базы данных было сделано прямое указание в docker-compose файле:

### App Dockerfile

```
FROM python:3.11-slim

WORKDIR /parser_api

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Celery Dockerfile

    ```
    FROM python:3.10-alpine3.19

    WORKDIR /run_celery

    COPY . .
    RUN pip3 install -r requirements.txt

    CMD uvicorn main:app --host localhost --port 8001

    ```

## Создание docker-compose

```
version: '3.8'

services:
  fastapi_app:
    build:
      context: ./app
      dockerfile: Dockerfile
    ports:
      - "8000:80"
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - backend

  parser_api:
    build:
      context: ./parser_api
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    env_file:
      - .env
    depends_on:
      - db
      - redis
    networks:
      - backend

  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  redis:
    image: redis:6
    ports:
      - "6379:6379"
    networks:
      - backend

  celery_worker:
    build:
      context: ./parser_api
      dockerfile: Dockerfile
    command: ["celery", "-A", "celery_main.celery_app", "worker", "--loglevel=info"]
    env_file:
      - .env
    depends_on:
      - redis
      - db
    networks:
      - backend

  pgadmin:  
    image: dpage/pgadmin4
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - backend

volumes:
  postgres_data:

networks:
  backend:
    driver: bridge

```
