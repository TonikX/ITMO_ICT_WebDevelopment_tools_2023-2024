# Лабораторная работа 3
## Цель лабораторной работы
Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с базой данных и вызывать парсер через API и очередь.

Docker — это платформа для разработки, доставки и запуска приложений в контейнерах. Контейнеры позволяют упаковать приложение и все его зависимости в единый образ, который можно запускать на любой системе, поддерживающей Docker, что обеспечивает консистентность среды выполнения и упрощает развертывание. Docker помогает ускорить разработку, повысить гибкость и масштабируемость приложений.

Сначала был разработан один контейнер для парсинга и приложения из первой лабораторной работы. Затем был добавлен отдельный контейнер для парсинга.
## Описание заданий
## Задание 1

1. Создание FastAPI приложения: Создано в рамках лабораторной работы номер 1

2. Создание базы данных: Создано в рамках лабораторной работы номер 1

3. Создание парсера данных: Создано в рамках лабораторной работы номер 2

4. Реализуйте возможность вызова парсера по http. Для этого можно сделать отдельное приложение FastAPI для парсера или воспользоваться библиотекой socket или подобными.

5. Разработка Dockerfile: Необходимо создать Dockerfile для упаковки FastAPI приложения и приложения с парсером. В Dockerfile указать базовый образ, установить необходимые зависимости, скопировать исходные файлы в контейнер и определить команду для запуска приложения. Зачем: Docker позволяет упаковать приложение и все его зависимости в единый контейнер, что обеспечивает консистентность среды выполнения и упрощает развертывание.

6. Создание Docker Compose файла: Необходимо написать docker-compose.yml для управления оркестром сервисов, включающих FastAPI приложение, базу данных и парсер данных. Определите сервисы, укажите порты и зависимости между сервисами. Зачем: Docker Compose упрощает управление несколькими контейнерами, позволяя вам запускать и настраивать все сервисы вашего приложения с помощью одного файла конфигурации.



## Задание 2. Вызов парсера из FastAPI

Эндпоинт в FastAPI для вызова парсера: Необходимо добавить в FastAPI приложение ендпоинт, который будет принимать запросы с URL для парсинга от клиента, отправлять запрос парсеру (запущенному в отдельном контейнере) и возвращать ответ с результатом клиенту. 

Это позволит интегрировать функциональность парсера в ваше веб-приложение, предоставляя возможность пользователям запускать парсинг через API.


## Задание 3. Вызов парсера из FastAPI через очередь

Как это работает: Celery — это асинхронная очередь задач, которая позволяет легко распределять и выполнять задачи в фоне. 

Redis используется как брокер сообщений, хранящий задачи, которые должны быть выполнены. При получении HTTP-запроса, задача ставится в очередь Redis, и Celery-воркер обрабатывает её в фоне. Docker Compose позволяет легко настроить и запустить Celery, Redis и ваше FastAPI приложение как отдельные контейнеры, работающие в одной сети. Это упрощает управление зависимостями и конфигурацией всех компонентов системы. 

- Установить Celery и Redis: Необходимо добавить зависимости для Celery и Redis в проект. Celery будет использоваться для обработки задач в фоне, а Redis будет выступать в роли брокера задач и хранилища результатов. Зачем: Celery и Redis позволяют организовать фоновую обработку задач, что полезно для выполнения длительных или ресурсоемких операций без блокировки основного потока выполнения.

- Настроить Celery: Необходимо создать файл конфигурации для Celery. Определить задачу для парсинга URL, которая будет выполняться в фоновом режиме. Зачем: Настройка Celery позволит асинхронно обрабатывать задачи, что улучшит производительность и отзывчивость вашего приложения.

- Обновить Docker Compose файл: Необходимо добавить сервисы для Redis и Celery worker в docker-compose.yml. Определите зависимости между сервисами, чтобы обеспечить корректную работу оркестра. Зачем: Это позволит вам легко управлять всеми сервисами вашего приложения, включая асинхронную обработку задач, с помощью одного файла конфигурации.

- Эндпоинт для асинхронного вызова парсера: Необходимо добавить в FastAPI приложение маршрут для асинхронного вызова парсера. Маршрут должен принимать запросы с URL для парсинга, ставить задачу в очередь с помощью Celery и возвращать ответ о начале выполнения задачи. Зачем: Это позволит запускать парсинг веб-страниц в фоне, что улучшит производительность и пользовательский опыт вашего приложения.
### Dockerfile
    FROM python:3.10-slim-buster as builder
    
    RUN apt-get update
    
    RUN pip install poetry
    COPY poetry.lock pyproject.toml /
    RUN poetry config virtualenvs.create false \
        && poetry install --no-interaction --no-dev\
        && rm -rf pyproject.toml poetry.lock
    
    WORKDIR /qr_test
    COPY . /qr_test
    
    CMD uvicorn src.main:app --host 0.0.0.0 --port 8001

### Docker-сompose.yaml - с учетом добавления контейнера parser
    version: "3.10"
    services:
      app:
        build:
          context: .
        env_file: .env
        depends_on:
          - db
        ports:
          - "8001:8001"
        command: uvicorn src.main:app --host 0.0.0.0 --port 8001
        networks:
          - backend
        restart: always
    
      db:
        image: postgres
        restart: always
        #env_file: .env
        environment:
          - POSTGRES_PASSWORD=postgres
          - POSTGRES_USER=postgres
          - POSTGRES_DB=hfm
          - POSTGRES_PORT=5432
        volumes:
          - postgres_data:/var/lib/postgresql/data/
        ports:
          - "5432:5432"
        networks:
          - backend
    
      celery:
        restart: always
        build: .
        command: celery -A src.celery worker -B -l INFO
        volumes:
          - .:/usr/src/lab
        env_file: .env
        depends_on:
          - db
          - redis
          - parser
        networks:
          - backend
      parser:
        restart: always
        build: .
        command: uvicorn src.main2:app --host 0.0.0.0 --port 80
        volumes:
          - .:/usr/src/lab
        env_file: .env
        depends_on:
          - db
        ports:
          - "8002:80"
        networks:
          - backend
      redis:
        image: redis
        ports:
          - "6379:6379"
        networks:
          - backend
    
    
    volumes:
      postgres_data:
    
    networks:
      backend:
         driver: bridge

### pyproject.toml
    [tool.poetry]
    name = "lab"
    version = "0.1.0"
    description = ""
    authors = ["Maria Antonova <mariaantonova261@gmail.com>"]
    
    [tool.poetry.dependencies]
    python = "^3.10"
    sqlmodel = "^0.0.18"
    SQLAlchemy = "^2.0.30"
    pydantic = "^2.7.1"
    fastapi = "^0.111.0"
    uvicorn = "^0.29.0"
    aiohttp = "^3.9.5"
    alembic = "^1.13.1"
    celery = "^5.4.0"
    redis = "^5.0.4"
    psycopg2-binary = "^2.9.9"
    passlib = "^1.7.4"
    PyJWT = "^2.8.0"
    bs4 = "^0.0.2"
    
    [tool.poetry.dev-dependencies]
    
    [build-system]
    requires = ["poetry-core>=1.0.0"]
    build-backend = "poetry.core.masonry.api"
### parse2.py
    parse_router = APIRouter(prefix="", tags=["parser"])
    
    
    @parse_router.post("/parse")
    async def parse(url: str, session=Depends(get_session)):
        sqlalchemy_worker = SqlalchemyWorker(session)
        try:
            async with aiohttp.ClientSession() as request_session:
                response = await request_session.get(url)  #парсер запрашивает html
                response.raise_for_status()
                html = await response.text()
                parse_and_save(url, html, sqlalchemy_worker)
                #parse_url_content.delay(url, html, sqlalchemy_worker) # вызов задачи
                return {"message": "Parsing is started"}
        except aiohttp.client.ClientConnectorError as e:
            raise fastapi.HTTPException(status_code=500, detail=str(e))
### parse.py
    from fastapi import APIRouter
    from fastapi import Depends
    
    from src.settings.connection import get_session
    from src.tasks.parser_url_content import parse_url_content
        parse_router = APIRouter(prefix="", tags=["parser"])
    
    @parse_router.post("/parse")
    async def parse(url: str, session=Depends(get_session)):
        #sqlalchemy_worker = SqlalchemyWorker(session)
        parse_url_content.delay(url)  # вызов задачи для celery
        return {"message": "Parsing is started"}

### celery.py
    import os
    
    import requests
    from celery import Celery
    from src.adapters.db import SqlalchemyWorker
    from src.repos.parser import parse_and_save
    
    celery_app = Celery(__name__)
    celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
    celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
    
    
    import aiohttp
    
    from src.adapters.db import SqlalchemyWorker
    from src.celery import celery_app
    from src.repos.parser import parse_and_save
    
    
    @celery_app.task(name="parse_url_content") # задача celery - она выполняется синхронно
    def parse_url_content(url: str): #метод
        #parse_and_save(url, html, sqlalchemy_worker)
        with requests.Session() as request_session:
            full_url = f'http://parser/parse?url={url}'
            response = request_session.post(full_url)
            response.raise_for_status()
            #html = await response.text()
            #parse_url_content.delay(url, html, sqlalchemy_worker) # вызов задачи
            return {"message": "Parsing is started"}

##Вывод
В рамках данной лабораторной работы были получены навыки по настройки и использования асинхронной очереди задач в реальном приложении

