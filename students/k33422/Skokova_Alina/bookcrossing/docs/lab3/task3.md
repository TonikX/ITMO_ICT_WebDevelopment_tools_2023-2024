# Задача 3. Вызов парсера из FastAPI через очередь

## 1. Установить Celery и Redis

Были дбавлены зависимости для Celery и Redis в проект. Celery будет использоваться для обработки задач в фоне, а Redis будет выступать в роли брокера задач и хранилища результатов.

## 2. Настроить Celery

Был создан файл конфигурации для Celery. Была определена задача для парсинга URL, которая будет выполняться в фоновом режиме.

**`tasks.py`**

```python
from celery import Celery
import requests

app = Celery('tasks', broker='redis://redis:6379')

@app.task
def db_parse_celery(urls, num):
    params = {'num': f'{num}'}
    response = requests.post('http://parser:8010/parse', params=params, json=urls)
    return response.json()
```

## 3. Обновить Docker Compose файл

Были добавлены сервисы для Redis и Celery worker в docker-compose.yml. Были определены зависимости между сервисами, чтобы обеспечить корректную работу оркестра.

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

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 5s

  celery:
    build:
      context: ./app_bookcrossing
    command: celery -A app.tasks worker --loglevel=info
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
```

## 4. Эндпоинт для асинхронного вызова парсера:

Был добавлен в FastAPI приложение маршрут для асинхронного вызова парсера. Маршрут принимает запросы с URL для парсинга, ставит задачу в очередь с помощью Celery и возвращает ответ о начале выполнения задачи.

```python
@app.post("/db_parse_aync", tags=['parser'])
def db_parse_async(urls: List[str], num: int = 1) -> TypedDict('Response', {"status": int, "message": str}):
    response = db_parse_celery.delay(urls, num)
    return {"status": 200, "message": "Parsing task is called"}
```