# Docker Compose

Docker Compose — это инструмент для определения и запуска многоконтейнерных приложений Docker. Он позволяет описывать сервисы,
сети и тома, необходимые для приложения, в единственном файле `docker-compose.yml`. Docker Compose упрощает процесс
развертывания и управления приложениями, состоящими из нескольких контейнеров.

## Объяснение

```yaml
version: "3.4"
```

- Указывает версию синтаксиса Docker Compose. Версия 3.4 обеспечивает совместимость с большинством функций.

```yaml
services:
```

- Определяет сервисы, составляющие приложение.

```yaml
  database:
    container_name: database
    image: postgres:14.1-alpine
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    volumes:
      - db_data:/var/lib/postgresql/data
    env_file:
      - .env
    ports:
      - "5432:5432"
```

- Сервис базы данных PostgreSQL.
- Использует образ `postgres:14.1-alpine`.
- Определяет переменные окружения для конфигурации базы данных, получая значения из файла `.env`.
- Монтирует именованный том `db_data` для сохранения данных базы данных.
- Проксирует порт 5432 контейнера на порт 5432 хоста.

```yaml
  redis:
    container_name: redis
    image: redis:7.2.4
    ports:
      - "6379:6379"
```

- Сервис Redis.
- Использует образ `redis:7.2.4`.
- Проксирует порт 6379 контейнера на порт 6379 хоста.

```yaml
  app:
    container_name: app
    build:
      context: .
      dockerfile: Dockerfile
    command: python -m uvicorn main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - database
      - redis
```

- Сервис веб-приложения.
- Собирает образ из Dockerfile в текущей директории.
- Запускает команду `python -m uvicorn main:app --host 0.0.0.0 --port 8000` для запуска приложения.
- Проксирует порт 8000 контейнера на порт 8000 хоста.
- Загружает переменные окружения из файла `.env`.
- Зависит от сервисов `database` и `redis`, гарантируя, что они будут запущены перед `app`.

```yaml
  celery_worker:
    container_name: celery_worker
    build:
      context: .
      dockerfile: Dockerfile
    command: python -m celery -A celery_worker.app worker
    env_file:
      - .env
    depends_on:
      - app
```

- Сервис воркера Celery.
- Собирает образ из Dockerfile в текущей директории.
- Запускает команду `python -m celery -A celery_worker.app worker` для запуска воркера Celery.
- Загружает переменные окружения из файла `.env`.
- Зависит от сервиса `app`, гарантируя, что `app` будет запущен перед `celery_worker`.

```yaml
volumes:
  db_data:
```

- Определяет именованный том `db_data` для хранения данных базы данных.
