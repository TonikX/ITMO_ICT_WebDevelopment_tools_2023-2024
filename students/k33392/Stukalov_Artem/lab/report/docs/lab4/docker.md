# Докер

Финально упакуем все приложени в Docker и будем использовать для звауска docker compose.

```Dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR /app
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev
COPY . .
```

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres_pwd
      - POSTGRES_DB=api
    volumes:
      - ./postgres:/var/lib/postgresql/data
    expose:
      - 5432
    restart: always

  api:
    build:
      context: .
      dockerfile: Dockerfile
    tty: true
    env_file:
      - .env
    ports:
      - 3000:8000
    depends_on:
      - db
    command: poetry run python -m uvicorn src.web_api.main:app --host 0.0.0.0 --port 8000
    healthcheck:
      test: ['CMD', 'pg_isready']
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis
    expose:
      - 6379
    restart: always

  url_parser:
    build:
      context: .
      dockerfile: Dockerfile
    command: poetry run celery -A src.url_parser.main  worker --loglevel=info
    restart: always
    env_file:
      - .env
    depends_on:
      - redis
      - api
```
