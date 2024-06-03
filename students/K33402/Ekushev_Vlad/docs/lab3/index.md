# Отчёт

## Задача лабораторной работы

Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с базой данных и вызывать парсер через API и очередь.

## Стек

- `poetry` - для управления зависимостями и venv
- `fastapi`
- `uvicorn`
- `alembic`
- `sqlmodel`
- `jose` - генерация JWT токенов
- `celery`
- `redis`

## Структура папок

```bash
├── README.md
├── .env.example
├── pyproject.toml
├── poetry.lock
├── alembic.ini
├── migrations
├── scripts
├── tests
└── services
    └── app
        ├── core
        ├── routes
        ├── services
        ├── models
        └── main.py
    └── parser
        ├── config.py
        ├── celery_app.py  -- Таски Celery
        ├── database.py    -- Утилиты для общения с PostgreSQL
        └── main.py        -- FastAPI приложение
```

## Запуск

Запуск проекта осуществляется командой `docker compose up`.

Миграции применяются через `poetry run alembic upgrade head`
