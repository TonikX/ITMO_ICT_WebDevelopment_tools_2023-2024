### `Dockerfile`

Этот Dockerfile определяет среду для сборки приложения FastAPI и Celery worker.

- **Базовый образ**: Использует официальный образ Python 3.8.
- **Рабочая директория**: Устанавливает рабочую директорию на /app.
- **Копирование кода приложения**: Копирует директории web_api и url_parser, а также файл requirements.txt в образ.
- **Установка зависимостей**: Устанавливает зависимости Python, указанные в файле requirements.txt.

```Dockerfile
FROM python:3.8

WORKDIR /app

COPY ./web_api /app/web_api
COPY ./url_parser /app/url_parser
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt 
```

### `docker-compose.yml`

```docker
version: '3.8'

# Определяет четыре сервиса: api (приложение FastAPI), 
# db (база данных PostgreSQL), redis (брокер Redis) и worker (Celery worker).
services:
  # Сборка приложения FastAPI, открытие его на порту 8000
  # и установка переменных среды из файла .env.
  api:
    container_name: trip_fastapi
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
    command: uvicorn web_api.main:app --reload --host 0.0.0.0
    environment:
      SECRET_KEY: ${SECRET_KEY}
      ALGORITHM: ${ALGORITHM}
      DB_USER: ${DB_USER}
      DB_NAME: ${DB_NAME}
      DB_PASS: ${DB_PASS}
      DB_HOST: "db"
    depends_on:
      - db

  # Использует последний образ PostgreSQL, открывает его на порту 5432 и 
  # устанавливает переменные среды для учетных данных базы данных.
  db:
    container_name: trip_fastapi_postgres 
    image: postgres:latest
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  # redis: Использует образ Redis, открывает его на порту 6379.
  redis:
    image: redis
    ports:
      - "6379:6379"
    restart: always

  # worker: Сборка Celery worker, использование того же образа, что и приложение 
  # FastAPI, и запуск команды Celery worker.
  worker:
    build:
      context: .
      dockerfile: Dockerfile 
    command: celery -A url_parser.main worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - redis
      - api
    
volumes:
  postgres_data:
```