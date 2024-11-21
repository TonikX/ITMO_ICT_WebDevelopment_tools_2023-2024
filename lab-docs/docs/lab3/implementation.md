# Реализация

## Что будет сделано?

Мы получим следующую файловую структуру:

- postgres
    - Dockerfile
- app_main
    - app
    - Dockerfile
- app_parser
    - parser_threadingP
        - main.py
        - ...
    - setup.py
    - tasks.py
    - main.py
    - Dockerfile
- docker-compose.yaml

И следующее содержания docker-compose.yaml файла:

```yaml
services:
  postgres:
    # Ссылакется на папку с postgres
    build: postgres/
    # БД на хосте будет доступно по порту 5100
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d task_manager"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
    ports:
      - 5100:5432


  app_main:
    build: app_main/
    ports:
      - 8100:8100
    depends_on:
      postgres:
        condition: service_healthy
        # Перезагружается если сервис перезагрузился
        restart: true


  redis:
    image: 'redis:alpine'
    ports:
      - 6379:6379
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 5s

  celery:
    build: app_parser/
    command: "celery -A tasks:celery worker -l info"
    healthcheck:
      test: celery -A tasks:celery  status
      interval: 10s
      timeout: 10s
      retries: 10
      start_period: 5s
    depends_on:
      redis:
        condition: service_healthy

  app_parser:
    build: app_parser/
    ports:
      - 8200:8200
    command: "fastapi run main.py --proxy-headers --port 8200"  
    depends_on:
      app_main:
        condition: service_started
      celery:
        condition: service_healthy
```

## Контейнеризация БД

Создадим директорию `postgres` в корне проекта. Добавим в нее `Dockerfile` с конфигурацией БД.

```Dockerfile
FROM postgres
ENV POSTGRES_PASSWORD 786811
ENV POSTGRES_DB task_manager
EXPOSE 5432
```

Добавим в `docker-compose.yaml` следующий строки:

```yaml
services:
  postgres:
    # Ссылакется на папку с postgres
    build: postgres/
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d task_manager"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
    # БД на хосте будет доступно по порту 5100
    ports:
      - 5100:5432
```

Структура проекта:

- postgres
    - Dockerfile
- docker-compose.yaml

## Контейнеризация API для планировщика задач

Создадим в проекте папку `app_main`. В ней создадим Dockerfile и папку `app` с
исходным кодом приложения.

Изменим ссылку на БД в `.env` файле приложения. Заменим `localhost` на `postgres`,
потому что теперь БД у нас будет находиться в сервисе `postgres`, а не на хосте.
Получим:
`DB_ADMIN=postgresql://postgres:786811@postgres:5432/task_manager`

Примечание: если бы наш сервис с БД в docker-compose.yaml назывался `db`, то
мы бы заменили `localhost` на `db`

Также добавим `Dockerfile`, который соберет наше приложение:

```Dockerfile
FROM python:3.12.3-alpine3.19
# requirements идут первыми, чтобы кэш не изменялся при изменении в приложении.
# То есть при изменениях в app без изменений в requirements,
# requirements не будут устанавливаться  заново, а будут подгружаться из кэша
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# copy app
WORKDIR /app
COPY /app .
EXPOSE 8100
CMD ["fastapi", "run", "/app/endpoints/endpoints.py", "--proxy-headers", "--port", "8100"]
```

В `docker-compose.yaml` добавим сервис для нашего приложения:

```yaml
  app_main:
    build: app_main/
    ports:
      - 8100:8100
    depends_on:
      postgres:
        condition: service_healthy
        # Перезагружается если сервис перезагрузился
        restart: true
```

Структура проекта на текущий момент:

- postgres
    - Dockerfile
- app_main
    - app
    - Dockerfile
- docker-compose.yaml

## Контейнеризация парсера

### Изменим URL обращения к API приложения

В parser_threading из предудыдущей лабораторной нам надо изменить URL для обращения в API приложения,
потому что раньше мы обращались к localhost, а сейчас нам надо обращаться к app_main. Для этого
будем использовать переменные окружения. Добавим следующий код в начало `main.py`:

```python

import os

if "BACKEND_URL" not in os.environ:
    raise RuntimeError('environment variable "BACKEND_URL" is not set')
BACKEND_URL = os.environ["BACKEND_URL"]
```

Теперь мы можем обращаться в API приложения при помощи это переменной. Пример:

```python
url =  f"{BACKEND_URL}/project/"
response = requests.post(url).json()

```

### Создадим из `parser_threading` пакет python

Создадим дирректорию `app_parser` в корневой и переместим в неё `parser_threading`
и добавим `setup.py` со следующим содержанием:

```python

from setuptools import setup, find_packages

setup(
    name='parser_threading',
    version='0.1',
    packages=find_packages('.')
)
```

Получаем:

- app_parser
    - parser_threading
        - main.py
        - ...
    - setup.py

### Сделаем функцию для добавления задачи парсинга в `celery`

Примечание: `celery` у нас будет отдельным сервисом, который будет выполнять задачи в фоне.
Для хранения списка задача `celery` будет использовать `redis`, который тоже мы сделаем отдельным сервисом.
Но создание задач `celery` делается через питоновску библиотеку. Вот такая многоходовочка.

Создадим в `app_parser` файл `tasks.py`, в котором мы сделаем функцию для добавления задачи парсинга в `celery`.
Вот код:

```python
from celery import Celery
from parser_threading.main import main

# качестве broker мы указываем ссылку на redis
# Пока у нас еще не поднят микросервис для redis, мы сделаем это далее по коду
celery = Celery('tasks', broker='redis://redis:6379')


@celery.task
def parse_task(token):
    main(token)

```

Получается следующая структура:

- app_parser
    - parser_threading
        - main.py
        - ...
    - setup.py
    - tasks.py

Теперь нам осталось превратить `parser_threading` в FastAPI приложение
и добавить celery с redis как сервисы

### Превратим `app_parser` в fastAPI приложение

Создадим в `app_parser` файл `main.py` и напишем туда следующий код:

```python
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
import requests
from tasks import parse_task

import os


if "BACKEND_URL" not in os.environ:
    raise RuntimeError('environment variable "BACKEND_URL" is not set')
BACKEND_URL = os.environ["BACKEND_URL"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()



@app.get('/')
def parse_data(token: Annotated[str, Depends(oauth2_scheme)]):
    response = check_backend_connection(token)
    check_token(response)
    try:
        parse_task.delay(token)
    except Exception as e:
        raise HTTPException(
            status_code=501,
            detail='Server error while parsing: \n'+ str(e)
        )
    return {'msg': 'Процесс парсинга запустился, подождите 10 секунд'}


def check_backend_connection(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(
            f'{BACKEND_URL}/user/',
            headers=headers)
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=404,
            detail=f'Invalid variable BACKEND_URL or backend is down. BACKEND_URL:{BACKEND_URL}'
        )
    return response

def check_token(response):
    status_code = response.status_code
    if status_code == 403:
        raise HTTPException(status_code=403, detail='Invalid token')
    elif status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f'Invalid variable BACKEND_URL or backend is unreachable. BACKEND_URL:{BACKEND_URL}'
        )
```

### Напишем Dockerfile для app_parser

Добавим Dockerfile в `app_parser` и получим:

- app_parser
    - parser_threading
        - main.py
        - ...
    - setup.py
    - tasks.py
    - main.py
    - Dockerfile

В Dockerfile соберем наш проект:

```Dockerfile
FROM python:3.12.3-alpine3.19
# install requirements
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./parser_threading ./parser_threading
RUN pip install -e ./parser_threading

COPY ./main.py .
COPY ./tasks.py .
# set ENV variable for backend
ENV BACKEND_URL="http://app_main:8100"
# run parser fastapi app
EXPOSE 8200
CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "8200"]

```

### Создадим сервисы для celery, redis и app_parser

В docker-compose добавим сервисы:

```yaml
  redis:
    image: 'redis:alpine'
    ports:
      - 6379:6379
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 5s

  celery:
    build: app_parser/
    command: "celery -A tasks:celery worker -l info"
    healthcheck:
      test: celery -A tasks:celery  status
      interval: 10s
      timeout: 10s
      retries: 10
      start_period: 5s
    depends_on:
      redis:
        condition: service_healthy

  app_parser:
    build: app_parser/
    ports:
      - 8200:8200
    command: "fastapi run main.py --proxy-headers --port 8200"  
    depends_on:
      app_main:
        condition: service_started
      celery:
        condition: service_healthy
```

Наше приложение готово к работе!
