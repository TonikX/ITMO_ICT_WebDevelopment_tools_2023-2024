# Задача 1. Упаковка FastAPI приложения, базы данных и парсера данных в Docker

## 1. Создание FastAPI приложения 

Создано в рамках лабораторной работы номер 1.

## 2. Создание базы данных

Создано в рамках лабораторной работы номер 1.

## 3. Создание парсера данных

Создано в рамках лабораторной работы номер 2.

## 4. Реализуйте возможность вызова парсера по http 

Для этого было сделано отдельное приложение FastAPI для парсера.

**`main.py`**

```python
from typing import List
from fastapi import FastAPI, HTTPException
from typing_extensions import TypedDict

from .task2_threading import main

app = FastAPI()

@app.post("/parse")
def parse(urls: List[str], num: int) -> TypedDict('Response', {"status": int, "message": str}):
    main(urls, num)
    return {"status": 200, "message": "Parsing completed"}
```

## 5. Разработка Dockerfile

**Dockerfile для для упаковки FastAPI приложения:**

```docker
FROM python:3.12.3-alpine3.19

WORKDIR /src

COPY requirements.txt requirements.txt

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /src/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile для для упаковки приложения с парсером:**

```docker
FROM python:3.12.3-alpine3.19

WORKDIR /src

COPY requirements.txt requirements.txt

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./parser /src/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
```

## 6. Создание Docker Compose файла

Был написан файл **`docker-compose.yml`** для управления оркестром сервисов, включающих FastAPI приложение, базу данных и парсер данных.

```docker
version: '3.8'

services:
  postgres:
    image: postgres:latest
    container_name: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 1234
      POSTGRES_DB: bookcross_db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d bookcross_db"]
      interval: 45s
      timeout: 45s
    ports:
      - "5433:5432"

  bookcrossing-app:
    build: 
      context: ./app_bookcrossing
    container_name: bookcrossing
    ports:
      - "8001:8000"
    depends_on:
      postgres:
        condition: service_healthy

  parser-app:
    build: 
      context: ./app_parser
    container_name: parser
    ports:
      - "8020:8010"
    depends_on:
      postgres:
        condition: service_healthy
    

```