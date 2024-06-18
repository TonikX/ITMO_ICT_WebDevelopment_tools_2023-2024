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
FROM python:3.9.19-alpine3.20

WORKDIR ./app

COPY . .
RUN pip3 install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8000
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
version: '3.9'
services:
main_db:
container_name: main_db
image: postgres
restart: always
environment: - POSTGRES_PASSWORD=1 - POSTGRES_USER=postgres - POSTGRES_DB=web_data - POSTGRES_PORT=5432
volumes: - postgres_data:/var/lib/postgresql/data/
ports: - "5432:5432"
networks: - backend

app:
container_name: app
build:
context: ./app
env_file: .env
depends_on: - main_db - redis
ports: - "8000:8000"
command: uvicorn main:app --host 0.0.0.0 --port 8000
networks: - backend
restart: always

celery_run:
container_name: celery_run
build:
context: ./run_celery
env_file: .env
depends_on: - main_db - redis
ports: - "8001:8001"
command: uvicorn main:app --host 0.0.0.0 --port 8001
networks: - backend
restart: always

celery_start:
build:
context: ./run_celery
container_name: celery_start
command: celery -A celery_start worker --loglevel=info
restart: always
depends_on: - redis - app - main_db
networks: - backend

redis:
image: redis
ports: - "6379:6379"
networks: - backend

volumes:
postgres_data:

networks:
backend:
driver: bridge

```
