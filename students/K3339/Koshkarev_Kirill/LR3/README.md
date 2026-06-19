# Лабораторная работа №3 — Docker, источники данных и очереди

**Дисциплина:** Web-разработка

Упаковка FastAPI-приложения (ЛР1), базы данных и парсера (ЛР2) в Docker,
вызов парсера по HTTP и через очередь задач Celery + Redis.

---

## Архитектура (6 сервисов в docker-compose)

```
                 ┌───────────────────────────────────────────┐
client ─HTTP→    │  api (FastAPI, :8000)                      │
                 │   ├─ /parser/sync  ──HTTP──►  parser (:8001)│──┐
                 │   └─ /parser/async ──►  очередь Redis        │  │
                 └───────────────┬───────────────┬────────────┘  │
                                 │               │               │
                            ┌────▼────┐     ┌────▼─────┐    ┌─────▼─────┐
                            │ redis   │◄────│ worker   │    │ db        │
                            │ (broker)│     │ (Celery) │───►│ Postgres  │
                            └────▲────┘     └──────────┘    │ parsed_   │
                                 │          ┌──────────┐    │  pages    │
                                 └──────────│ beat     │    └───────────┘
                                            │(периодич.)│
                                            └──────────┘
```

| Сервис | Образ / команда | Назначение |
|---|---|---|
| `db` | `postgres:16-alpine` | база данных (из ЛР1) |
| `redis` | `redis:7-alpine` | брокер очереди и backend результатов Celery |
| `api` | `uvicorn app.main:app` :8000 | основное приложение (ЛР1 + интеграция парсера) |
| `parser` | `uvicorn parser.main:app` :8001 | сервис-парсер, вызывается по HTTP |
| `worker` | `celery -A worker.celery_app worker` | обработка фоновых задач парсинга |
| `beat` | `celery -A worker.celery_app beat` | периодические задачи (bonus) |

Все Python-сервисы собираются из **одного** `Dockerfile` (общий образ) и
различаются только командой запуска.

---

## Запуск

```bash
cd LR3
docker compose up --build
```

После старта:
- Swagger основного приложения: http://localhost:8000/docs
- Swagger сервиса-парсера: http://localhost:8001/docs

Остановить: `docker compose down` (с удалением данных БД: `docker compose down -v`).

---

## Подзадача 1 — упаковка в Docker

- **`Dockerfile`** — базовый образ `python:3.11-slim`, установка зависимостей из
  `requirements.txt`, копирование кода (`app`, `parser`, `worker`), команда запуска.
- **`docker-compose.yml`** — оркестрация всех сервисов, проброс портов,
  `depends_on` с `healthcheck` (api ждёт готовности БД, Redis и парсера).
- **Парсер вызывается по HTTP** — сервис `parser` (`parser/main.py`) с эндпоинтом
  `POST /parse`, который грузит страницу, извлекает `<title>` и пишет в БД.

База данных — **PostgreSQL** (в compose), та же схема, что в ЛР1; парсер
заполняет таблицу `parsed_pages`.

> **Асинхронная запись в БД.** Сохранение результатов парсинга выполняется
> неблокирующе: функция `parse_and_save_async` ([app/parsing.py](app/parsing.py))
> использует SQLAlchemy async + драйвер `asyncpg` (для PostgreSQL) или `aiosqlite`
> (для SQLite), `commit` идёт через `await`. Эндпоинт парсера `POST /parse` —
> `async def`, а Celery-задача запускает корутину через `asyncio.run`. Для async-
> движка используется `NullPool`, чтобы соединение не переиспользовалось между
> разными событийными циклами (важно для Celery, где каждая задача — новый цикл).

## Подзадача 2 — вызов парсера из FastAPI (синхронно)

Эндпоинт **`POST /parser/sync?url=...`** в основном приложении
([app/routers/parser.py](app/routers/parser.py)) по HTTP обращается к сервису
`parser` (адрес из переменной `PARSER_URL`), дожидается результата и возвращает
его клиенту.

```bash
curl -X POST "http://localhost:8000/parser/sync?url=https://example.com"
```

## Подзадача 3 — вызов парсера через очередь (Celery + Redis)

- **`worker/celery_app.py`** — конфигурация Celery (брокер и backend = Redis) и
  задача `parse_url_task(url)`, которая в фоне парсит страницу и сохраняет в БД.
- Эндпоинт **`POST /parser/async?url=...`** ставит задачу в очередь и сразу
  возвращает `task_id` (не блокируя клиента).
- Эндпоинт **`GET /parser/result/{task_id}`** возвращает статус и результат
  фоновой задачи.

```bash
# поставить задачу в очередь
curl -X POST "http://localhost:8000/parser/async?url=https://www.python.org"
# -> {"task_id": "...", "status_url": "/parser/result/..."}

# узнать результат
curl "http://localhost:8000/parser/result/<task_id>"

# посмотреть все распарсенные страницы в БД
curl "http://localhost:8000/parser/pages"
```

## Bonus — периодические задачи

В `worker/celery_app.py` настроен `beat_schedule`: задача
`count_parsed_pages_task` выполняется **каждую минуту** и логирует количество
распарсенных страниц. Запускается сервисом `beat`.

---

## Структура проекта

```
LR3/
├── app/                      # основное приложение (ЛР1 + интеграция парсера)
│   ├── main.py               # точка входа, подключение роутеров
│   ├── config.py             # настройки (БД, JWT, PARSER_URL, Celery/Redis)
│   ├── database.py           # engine/сессия SQLAlchemy
│   ├── models.py             # модели ЛР1 + ParsedPage
│   ├── init_db.py            # создание таблиц с ожиданием готовности БД
│   ├── parsing.py            # общая логика: загрузка + <title> + запись в БД
│   ├── routers/parser.py     # /parser/sync, /parser/async, /parser/result, /parser/pages
│   └── routers/...           # auth, users, hackathons, teams, tasks, submissions (ЛР1)
├── parser/
│   └── main.py               # отдельный сервис-парсер: POST /parse
├── worker/
│   └── celery_app.py         # Celery + задачи + расписание (beat)
├── Dockerfile                # единый образ для api/parser/worker/beat
├── docker-compose.yml        # оркестрация db, redis, api, parser, worker, beat
├── requirements.txt
└── smoke_test.py             # локальная проверка без Docker (SQLite + Celery eager)
```

---

## Локальная проверка без Docker

Логику можно проверить и без Docker (на SQLite, Celery в режиме `eager`):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python smoke_test.py
```

Тест проверяет: сервис-парсер `POST /parse`, синхронный вызов `/parser/sync`
(парсер поднимается в фоне), асинхронный вызов `/parser/async` (очередь Celery),
запись результатов в БД и список `/parser/pages`. Полная схема с PostgreSQL,
Redis и реальным воркером проверяется через `docker compose up`.

> Примечание: `psycopg2-binary` нужен только для PostgreSQL в Docker; при
> локальной проверке на SQLite его установка не обязательна.
```
