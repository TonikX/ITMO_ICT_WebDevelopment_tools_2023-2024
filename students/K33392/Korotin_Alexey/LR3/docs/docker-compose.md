# Структура файла docker-compose
```yaml
version: '3.10'
services:
  app-db:
    image: postgres:latest
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: db
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - ./volumes/app-db:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready" ]
      interval: 10s
      timeout: 5s
      retries: 5
  app:
    pull_policy: build
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://postgres:postgres@app-db:5432/db
    depends_on:
      app-db:
        condition: service_healthy
    ports:
      - "8000:8000"
  parser:
    pull_policy: build
    build:
      context: ../LR3
      dockerfile: Dockerfile
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    ports:
      - "8001:8000"
    environment:
      REDIS_HOST: redis://redis:6379/0
      BROKER: redis://redis:6379/0
    depends_on:
      - redis
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
  celery:
    build:
      context: ../LR3
      dockerfile: Dockerfile
    command: ["python", "-m", "celery", "-A", "celery_backend.app", "worker"]
    environment:
      REDIS_HOST: redis://redis:6379/0
      BROKER: redis://redis:6379/0
    depends_on:
      - redis
```
## Сетевое взаимодействие
В данном решении реализовано сетевое взаимодействие между контейнерами с использованием 
внутренней сети docker (docker internal network).

В качестве имен хостов во внутренней сети выступают имена контейнеров, поэтому мы можем использовать подобные конструкции:

`DATABASE_URL: postgresql://postgres:postgres@app-db:5432/db`

Здесь мы передаем URL для подключения к БД через переменную среды в контейнер app. 
Видим, что вместо адреса хоста БД используется название контейнера (`app-db`). 
Это возможно благодаря ранее упомянутой внутренней сети docker.
## Порядок запуска
Помимо всего прочего стоит отметить, что в данном конфигурационном файле обозначен порядок запуска контейнеров.
Так, контейнер `app` зависит от контейнера `app-db` (а точнее, от его здорового состояния), что логично, 
потому что контейнер приложения не может функционировать без контейнера БД.

Также запуск контейнеров `celery` и `parser` зависит от работы контейнера `redis` все по той же причине.