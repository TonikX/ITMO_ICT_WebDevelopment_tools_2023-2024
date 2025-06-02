## Лабораторная работа 3: Упаковка FastAPI приложения в Docker, Работа с источниками данных и Очереди

### Цель

Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с базой данных и вызывать парсер через HTTP и очередь задач (Celery + Redis).



## Структура проекта

```
project_root/
│
├── api_service/              # FastAPI API-сервис (основное приложение)
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── repository.py
│   ├── tasks.py
│   ├── celery_app.py
│   ├── database.py
│   ├── requests.py
│   ├── responses.py
│   ├── status_enum.py
│   └── requirements.txt
│
├── parser_service/           # FastAPI сервис–парсер
│   ├── main.py
│   ├── routes.py
│   ├── parser.py
│   ├── redis_listener.py
│   ├── requests.py
│   ├── responses.py
│   └── requirements.txt
│
├── docker-compose.yml
├── Dockerfile.api            # Dockerfile для api_service
├── Dockerfile.parser         # Dockerfile для parser_service
└── README.md                 # Инструкция по запуску (при необходимости)
```


## Подзадача 1. Упаковка FastAPI приложения и парсера в Docker


### 1.1. Dockerfile для API-сервиса

`api_service` — это FastAPI приложение, которое:

* Принимает запросы от клиента (`parse_sync`, `parse_async`, `status`, `result`).
* Сохраняет информацию о запросах в PostgreSQL (таблица `parse_requests`).
* Для асинхронного парсинга ставит задачу в очередь Celery (через Redis).

Ниже приведён пример `Dockerfile.api`, который упаковывает весь `api_service` в контейнер:

```dockerfile
# Dockerfile.api

# 1. Базовый образ с Python 3.10 (альтернативно можно взять slim-версию)
FROM python:3.10-slim

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Копируем requirements и устанавливаем зависимости
COPY api_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем исходники API-сервиса
COPY api_service/ .

# 5. Устанавливаем переменные окружения по умолчанию (при желании)
ENV DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/app_db
ENV REDIS_URL=redis://redis:6379/0
ENV TASK_QUEUE=parser:tasks
ENV RESULT_PREFIX=parser:results:

# 6. Открываем порт, на котором будет запущен FastAPI
EXPOSE 8000

# 7. Команда запуска uvicorn (асинхронная, для работы FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 1.2. Dockerfile для сервиса-парсера

`parser_service` — это FastAPI приложение, которое:

* Слушает HTTP-запросы на эндпоинте `/fetch` и выполняет парсинг (скачивает HTML по URL, извлекает `<title>` с помощью BeautifulSoup).
* Параллельно, в режиме слушателя (listener) слушает Redis-кью `parser:tasks`, обрабатывает задачи и кладёт результат в Redis с ключом `parser:results:{request_id}`.

```dockerfile
# Dockerfile.parser

# 1. Базовый образ Python
FROM python:3.10-slim

# 2. Рабочая директория
WORKDIR /app

# 3. Копируем и устанавливаем зависимости
COPY parser_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем исходники парсера
COPY parser_service/ .

# 5. Устанавливаем переменные окружения
ENV REDIS_URL=redis://redis:6379/0
ENV TASK_QUEUE=parser:tasks
ENV RESULT_PREFIX=parser:results:

# 6. Открываем порт для FastAPI (сервис-парсер может отвечать на HTTP, хотя основной поток – listener)
EXPOSE 8001

# 7. Команда запуска: uvicorn + запуск background listener в фоновом режиме через tmux/pm2/supervisor
# Здесь приведён пример запуска listener и FastAPI в одном процессе через shell-скрипт.
COPY start_parser.sh .
RUN chmod +x start_parser.sh

CMD ["./start_parser.sh"]
```

>
> * Внутри контейнера запускаются одновременно две задачи: FastAPI (для синхронных HTTP запросов) и listener (для обработки задач из очереди).
> * `python -u redis_listener.py` — запускает бесконечный цикл `start_listener`, см. `parser_service/redis_listener.py`:
>
>   ```python
>   import asyncio
>   import json
>   import os
>   import redis.asyncio as aioredis
>   from parser import fetch_html_and_title
>
>   TASK_QUEUE = os.getenv("TASK_QUEUE", "parser:tasks")
>   RESULT_PREFIX = os.getenv("RESULT_PREFIX", "parser:results:")
>
>   async def start_listener(redis: aioredis.Redis) -> None:
>       print("[listener] started, waiting for tasks…")
>       while True:
>           task = await redis.blpop(TASK_QUEUE, timeout=5)
>           if task is None:
>               continue
>
>           _, raw = task
>           payload = json.loads(raw)
>           req_id = payload["id"]
>           url = payload["url"]
>           print(f"[listener] got task id={req_id} url={url}")
>
>           try:
>               title, html = await fetch_html_and_title(url)
>               result = {"status": "success", "title": title, "html": html}
>           except Exception as err:
>               print(f"[listener] task failed: {err}")
>               result = {"status": "failure", "error": str(err)}
>
>           await redis.set(f"{RESULT_PREFIX}{req_id}", json.dumps(result), ex=3600)
>           print(f"[listener] stored result for id={req_id}")
>
>   async def main():
>       redis = aioredis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
>       try:
>           await start_listener(redis)
>       finally:
>           await redis.close()
>
>   if __name__ == "__main__":
>       asyncio.run(main())
>   ```

---

### 1.3. Docker Compose: `docker-compose.yml`

`docker-compose.yml` объединяет следующие сервисы:

* **db** — PostgreSQL (образ `postgres:15-alpine`).
* **redis** — Redis (образ `redis:6-alpine`).
* **api** — контейнер с FastAPI (`Dockerfile.api`).
* **parser** — контейнер с FastAPI + listener (`Dockerfile.parser`).
* **worker** — контейнер с Celery worker (использует код из `api_service/celery_app.py` и `api_service/tasks.py`).

```yaml
version: "3.9"

services:
  db:
    image: postgres:15-alpine
    container_name: postgres_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app_db
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    container_name: redis_cache
    restart: unless-stopped
    ports:
      - "6379:6379"

  parser:
    build:
      context: .
      dockerfile: Dockerfile.parser
    container_name: parser_service
    depends_on:
      - redis
    environment:
      REDIS_URL: "redis://redis:6379/0"
      TASK_QUEUE: "parser:tasks"
      RESULT_PREFIX: "parser:results:"
    ports:
      - "8001:8001"

  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: api_service
    depends_on:
      - db
      - redis
      - parser
    environment:
      DATABASE_URL: "postgresql+asyncpg://user:pass@db:5432/app_db"
      REDIS_URL: "redis://redis:6379/0"
      TASK_QUEUE: "parser:tasks"
      RESULT_PREFIX: "parser:results:"
    ports:
      - "8000:8000"

  worker:
    image: python:3.10-slim
    container_name: celery_worker
    working_dir: /app
    command: celery -A celery_app.celery_app worker --loglevel=info -Q api
    volumes:
      - ./api_service:/app
    depends_on:
      - api
      - redis
      - db
    environment:
      DATABASE_URL: "postgresql+asyncpg://user:pass@db:5432/app_db"
      REDIS_URL: "redis://redis:6379/0"
      TASK_QUEUE: "parser:tasks"
      RESULT_PREFIX: "parser:results:"

volumes:
  db_data:
```

> **Пояснения к `docker-compose.yml`:**
>
> * `db` и `redis` запускаются первыми, чтобы их могли использовать остальные сервисы.
> * `parser` зависит от `redis` (очереди задач).
> * `api` зависит от `db`, `redis` и `parser`.
> * `worker` (Celery) монтирует код из `api_service` и запускается с командой:
>
>   ```yaml
>   command: celery -A celery_app.celery_app worker --loglevel=info -Q api
>   ```
>
>   где `-A celery_app.celery_app` указывает Celery “app” (файл `api_service/celery_app.py`), а `-Q api` — очередь `api`, заданная в конфигурации Celery (см. `celery_app.py`).

---

## Синхронный и асинхронный HTTP-вызов парсера

### 2.1. Эндпоинты FastAPI (`api_service/routes.py`)

#### 2.1.1. Синхронный парсинг через HTTP

Эндпоинт `GET /parse_sync` отправляет HTTP-запрос на парсер (контейнер `parser_service`) и сразу ждёт ответа:

```python
@router.get("/parse_sync")
async def parse_sync(
        query: Annotated[ParseSyncQuery, Query()],
) -> SyncResult:
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        try:
            resp = await client.get(PARSER_HTTP, params={"url": query.url})
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    data = resp.json()
    return SyncResult(
        url=query.url,
        title=data["title"],
        html=data["html"]
    )
```

* `PARSER_HTTP = "http://parser:8001/fetch"` — URL парсера внутри сети Docker Compose.
* `ParseSyncQuery` (в `api_service/requests.py`) имеет поле `url: HttpUrl`.
* Возвращается модель `SyncResult` (в `api_service/responses.py`):

  ```python
  class SyncResult(BaseModel):
      title: str
      html: str
      url: HttpUrl
  ```

#### 2.1.2. Асинхронный парсинг (через очередь Celery)

Эндпоинт `POST /parse_async` создаёт запись в базе (таблица `parse_requests`), ставит задачу в очередь и возвращает `request_id` + статус:

```python
@router.post("/parse_async")
async def parse_async(
        payload: ParseAsyncCreate,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> ParseAsyncResponse:
    req = await Repo.create(session, str(payload.url))
    parse_url_task.delay(req.id, str(payload.url))
    return ParseAsyncResponse(request_id=req.id, status=req.status)
```

* `ParseAsyncCreate` (в `api_service/requests.py`):

  ```python
  class ParseAsyncCreate(BaseModel):
      url: HttpUrl = Field(..., example="https://example.com")
  ```
* `Repo.create()` (в `api_service/repository.py`) создаёт новую запись `ParseRequest`:

  ```python
  class ParseRepository:
      @staticmethod
      async def create(session: AsyncSession, url: str) -> ParseRequest:
          req = ParseRequest(url=url, status=StatusEnum.pending)
          session.add(req)
          await session.commit()
          await session.refresh(req)
          return req
  ```
* `parse_url_task.delay(req.id, str(payload.url))` — ставит задачу в очередь Celery (очередь `api`).

Эндпоинты для проверки статуса и получения результата:

```python
@router.get("/status/{request_id}")
async def status(
        request_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> StatusResponse:
    obj = await Repo.by_id(session, request_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    return StatusResponse(request_id=obj.id, status=obj.status)
```

```python
@router.get("/result/{request_id}")
async def result(
        request_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> ResultResponse:
    obj = await Repo.by_id(session, request_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    return ResultResponse(
        request_id=obj.id,
        status=obj.status,
        title=obj.title,
        html=obj.html_content,
    )
```

* `StatusResponse` и `ResultResponse` описаны в `api_service/responses.py`:

  ```python
  class StatusResponse(BaseModel):
      request_id: int
      status: StatusEnum

  class ResultResponse(BaseModel):
      request_id: int
      status: StatusEnum
      title: Optional[str] = None
      html: Optional[str] = None
  ```

> **Итог:**
>
> * `GET /parse_sync?url=...` — блокирующий синхронный вызов парсера.
> * `POST /parse_async {"url": "..."} ` — запись в БД + отправка задачи в Celery.
> * `GET /status/{id}` и `GET /result/{id}` — мониторинг и получение результата.

---

## Вызов парсера через очередь (Celery + Redis)


### 3.1. Настройка Celery

#### `api_service/celery_app.py`

```python
from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "api_service",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["api_service.tasks"],
)

# Очередь по умолчанию
celery_app.conf.task_default_queue = "api"
celery_app.conf.timezone = "UTC"
```

* `broker=REDIS_URL` — используется Redis как брокер сообщений (для передачи задач).
* `backend=REDIS_URL` — Redis же используется для хранения результатов (необязательно, но удобно).
* `include=["api_service.tasks"]` — указываем модуль с задачами.

---

### 3.2. Таск для парсинга в Celery

#### `api_service/tasks.py`

```python
import asyncio
import json
import os
from time import time, sleep

import redis
from celery import shared_task
from sqlalchemy import update

from api_service.celery_app import celery_app
from api_service.database import AsyncSessionLocal
from api_service.models import ParseRequest, StatusEnum

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
TASK_QUEUE = os.getenv("TASK_QUEUE", "parser:tasks")
RESULT_PREFIX = os.getenv("RESULT_PREFIX", "parser:results:")

@shared_task(name="api.parse_url", queue="api")
def parse_url_task(request_id: int, url: str) -> None:
    """
    1) Кладём задачу в Redis список TASK_QUEUE.
    2) Блокирующе ждём результат (до 30 секунд).
    3) Записываем результат в таблицу parse_requests.
    """
    # Подключаемся к Redis
    r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

    # 1) Отправляем в очередь
    payload = json.dumps({"id": request_id, "url": url})
    r.lpush(TASK_QUEUE, payload)

    # 2) Ожидаем результат в Redis под ключом RESULT_PREFIX{request_id}
    res_key = f"{RESULT_PREFIX}{request_id}"
    deadline = time() + 30
    result_data = None

    while time() < deadline:
        data = r.get(res_key)
        if data:
            result_data = json.loads(data)
            r.delete(res_key)
            break
        sleep(1)

    # Функция для записи результата в БД
    async def _write(status: StatusEnum, title: str | None = None, html: str | None = None):
        async with AsyncSessionLocal() as session:
            stmt = (
                update(ParseRequest)
                .where(ParseRequest.id == request_id)
                .values(status=status, title=title, html_content=html)
            )
            await session.execute(stmt)
            await session.commit()

    if not result_data:
        # Если Timeout
        asyncio.run(_write(StatusEnum.failure, title=None, html="Timeout waiting result"))
        return

    # Если есть результат
    if result_data.get("status") == "success":
        asyncio.run(_write(StatusEnum.success,
                          title=result_data.get("title"),
                          html=result_data.get("html")))
    else:
        asyncio.run(_write(StatusEnum.failure, html=result_data.get("error")))
```

> **Ключевые моменты кода:**
>
> 1. `shared_task(name="api.parse_url", queue="api")` — объявляем Celery-задачу под именем `api.parse_url`, которая поставится в очередь `api`.
> 2. Через `redis.Redis.from_url(REDIS_URL)` подключаемся к Redis.
> 3. `r.lpush(TASK_QUEUE, payload)` — кладём JSON `{ "id": request_id, "url": url }` в список `parser:tasks`.
> 4. Блокирующим циклом ждём, пока парсер не положит результат под ключ `parser:results:{id}` (максимум 30 секунд).
> 5. Запускаем асинхронную запись в PostgreSQL через SQLAlchemy Async (функция `_write`).

---

### 3.3. Сервис-парсер: получение задач из Redis и возвращение результата

#### `parser_service/redis_listener.py`

```python
import asyncio
import json
import os

import redis.asyncio as aioredis
from parser_service.parser import fetch_html_and_title

TASK_QUEUE = os.getenv("TASK_QUEUE", "parser:tasks")
RESULT_PREFIX = os.getenv("RESULT_PREFIX", "parser:results:")

async def start_listener(redis: aioredis.Redis) -> None:
    print("[listener] started, waiting for tasks…")
    while True:
        try:
            task = await redis.blpop(TASK_QUEUE, timeout=5)
            if task is None:
                continue

            _, raw = task
            payload = json.loads(raw)
            req_id = payload["id"]
            url = payload["url"]
            print(f"[listener] got task id={req_id} url={url}")

            try:
                title, html = await fetch_html_and_title(url)
                result = {"status": "success", "title": title, "html": html}
            except Exception as err:
                print(f"[listener] task failed: {err}")
                result = {"status": "failure", "error": str(err)}

            await redis.set(f"{RESULT_PREFIX}{req_id}", json.dumps(result), ex=3600)
            print(f"[listener] stored result for id={req_id}")
        except Exception as exc:
            print(f"[listener] error: {exc}")
            await asyncio.sleep(1)

async def main():
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
    redis = aioredis.from_url(redis_url, decode_responses=True)
    try:
        await start_listener(redis)
    finally:
        await redis.close()

if __name__ == "__main__":
    asyncio.run(main())
```

#### `parser_service/parser.py`

```python
import httpx
from bs4 import BeautifulSoup
from typing import Tuple

async def fetch_html_and_title(url: str, timeout: float = 10.0) -> Tuple[str, str]:
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        html_text = resp.text

    soup = BeautifulSoup(html_text, "lxml")
    title_tag = soup.find("title")
    title = title_tag.text.strip() if title_tag else ""
    return title, html_text
```

#### `parser_service/routes.py` (эндпоинт для синхронного парсинга)

```python
from fastapi import APIRouter, HTTPException, Query
from parser_service.parser import fetch_html_and_title
from parser_service.requests import FetchQuery
from parser_service.responses import FetchResponse

router = APIRouter()

@router.get(
    "/fetch",
    response_model=FetchResponse,
    summary="Скачать страницу и вернуть HTML"
)
async def fetch(query: Annotated[FetchQuery, Query(...)]):
    try:
        title, html = await fetch_html_and_title(str(query.url))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return FetchResponse(url=query.url, title=title, html=html)
```

* `FetchQuery` (в `parser_service/requests.py`):

  ```python
  class FetchQuery(BaseModel):
      url: HttpUrl = Field(..., example="https://example.com")
  ```
* `FetchResponse` (в `parser_service/responses.py`):

  ```python
  class FetchResponse(BaseModel):
      url: HttpUrl
      title: str
      html: str
  ```
* При запуске контейнера `parser_service` одновременно стартует этот эндпоинт (`/fetch`) и `start_listener`, который мониторит очередь.

---

### 3.4. Обновление Docker Compose для Celery и Redis

В `docker-compose.yml` (приведён выше) уже добавлены сервисы `redis` и `worker`.

* **redis**: образ `redis:6-alpine`, порт `6379`
* **worker**: запускает Celery worker с очередью `api`, монтирует `./api_service` внутрь контейнера

Пример клиента Celery внутри контейнера worker:

```yaml
worker:
  image: python:3.10-slim
  container_name: celery_worker
  working_dir: /app
  command: celery -A celery_app.celery_app worker --loglevel=info -Q api
  volumes:
    - ./api_service:/app
  depends_on:
    - api
    - redis
    - db
  environment:
    DATABASE_URL: "postgresql+asyncpg://user:pass@db:5432/app_db"
    REDIS_URL: "redis://redis:6379/0"
    TASK_QUEUE: "parser:tasks"
    RESULT_PREFIX: "parser:results:"
```

* `celery -A celery_app.celery_app worker` — указывает Celery искать объект `celery_app` в `api_service/celery_app.py`.
* `-Q api` — слушать очередь `api` (как настроено в `celery_app.conf.task_default_queue`).
* Через переменные окружения указываем параметры подключения к Redis и PostgreSQL.

После поднятия всех контейнеров (`docker-compose up --build`):

1. **parser\_service** слушает HTTP `/fetch` и Redis-очередь `parser:tasks`.
2. **api\_service** слушает HTTP `/parse_sync`, `/parse_async`, `/status/{}`, `/result/{}`.
3. **worker** (Celery) получает задачи из Redis-очереди `api`, выполняет `parse_url_task`, ставит новые сообщения в Redis для `parser_service`.

---

### 3.5. Эндпоинт для ставновки задачи через Celery

Подробно внутри `api_service/routes.py` рассмотрены:

```python
@router.post("/parse_async")
async def parse_async(
        payload: ParseAsyncCreate,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> ParseAsyncResponse:
    req = await Repo.create(session, str(payload.url))
    parse_url_task.delay(req.id, str(payload.url))
    return ParseAsyncResponse(request_id=req.id, status=req.status)
```

* Создаётся запись в таблице `parse_requests` (модель `api_service/models.py`):

  ```python
  class ParseRequest(Base):
      __tablename__ = "parse_requests"
      id: Mapped[int] = mapped_column(primary_key=True)
      url: Mapped[str]
      status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), default=StatusEnum.pending)
      title: Mapped[Optional[str]]
      html_content: Mapped[Optional[str]]
      created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, server_default=func.now())
      updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, server_default=func.now())
  ```
* Статус каждой задачи хранится в `ParseRequest.status` (enum `pending`, `processing`, `success`, `failure`).
* `parse_url_task.delay(req.id, str(payload.url))` — отсылает задачу в очередь `api` (Celery Worker).

#### Проверка статуса и получение результата

```python
@router.get("/status/{request_id}")
async def status(...):
    obj = await Repo.by_id(session, request_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return StatusResponse(request_id=obj.id, status=obj.status)
```

```python
@router.get("/result/{request_id}")
async def result(...):
    obj = await Repo.by_id(session, request_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return ResultResponse(
        request_id=obj.id,
        status=obj.status,
        title=obj.title,
        html=obj.html_content,
    )
```

---

### 3.6. Периодические задачи (опционально)

Celery поддерживает `beat` для периодических задач (cron-подобных). В `celery_app.py` добавляем конфиг `beat_schedule`:

```python
from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "api_service",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["api_service.tasks"],
)

celery_app.conf.task_default_queue = "api"
celery_app.conf.timezone = "UTC"

# Пример периодической задачи: очистка устаревших записей
celery_app.conf.beat_schedule = {
    "cleanup_parse_requests_every_midnight": {
        "task": "api.cleanup_parse_requests",
        "schedule": crontab(hour=0, minute=0),
    },
}
```

* Для этого потребуется добавить соответствующий таск в `api_service/tasks.py`:

  ```python
  @shared_task(name="api.cleanup_parse_requests")
  def cleanup_parse_requests():
      # Здесь логика очистки: удалить записи старше N дней
      pass
  ```
* В `docker-compose.yml` добавляем сервис `beat`:

  ```yaml
  beat:
    image: python:3.10-slim
    container_name: celery_beat
    working_dir: /app
    command: celery -A celery_app.celery_app beat --loglevel=info
    volumes:
      - ./api_service:/app
    depends_on:
      - redis
      - db
    environment:
      DATABASE_URL: "postgresql+asyncpg://user:pass@db:5432/app_db"
      REDIS_URL: "redis://redis:6379/0"
  ```

> **Важно:** Периодические задачи не были явно реализованы в коде, приведённом в `collected_py_files.json`, но этот пример показывает, как их добавить.

## Заключение

В ходе лабораторной работы были достигнуты следующие результаты:

1. **Контейнеризация**:

   * Созданы `Dockerfile.api` и `Dockerfile.parser` для упаковывания FastAPI-сервисов (API и парсера) вместе со всеми зависимостями.
   * Написан `docker-compose.yml`, объединяющий сервисы: PostgreSQL, Redis, API, парсер, Celery worker.
2. **Интеграция HTTP-вызова парсера**:

   * Реализован синхронный запрос к эндпоинту `/parse_sync` (парсер возвращает данные немедленно).
   * Эндпоинт `/parse_async`: добавление записи в БД, отправка задачи в Celery-очередь, возвращение `request_id`.
   * Эндпоинты `/status/{id}` и `/result/{id}` для мониторинга и получения результата парсинга.
3. **Асинхронная очередь на Celery + Redis**:

   * Настроен Celery (`api_service/celery_app.py`) для фоновых задач.
   * Создан таск `parse_url_task` (в `api_service/tasks.py`), который отправляет задачу парсеру через Redis, ждёт результат и записывает его в PostgreSQL.
   * Парсер (`parser_service/redis_listener.py`) слушает Redis-очередь `parser:tasks`, выполняет парсинг и кладёт результат в Redis с ключом `parser:results:{id}`.
   * Celery worker (`worker`) забирает таски из очереди `api` и выполняет их.

В результате:

* **FastAPI API** обрабатывает HTTP-запросы, хранит информацию о задаче в PostgreSQL.
* **Celery worker** асинхронно организует взаимодействие API ↔ Parser через Redis.
* **Parser service** по требованию загружает HTML-страницы, извлекает `<title>` и возвращает результат в очередь.
