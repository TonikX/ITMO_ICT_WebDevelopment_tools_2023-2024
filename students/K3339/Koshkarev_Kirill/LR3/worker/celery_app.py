"""Конфигурация Celery и фоновые задачи (подзадача 3).

Celery использует Redis как брокер сообщений (очередь задач) и как backend для
хранения результатов. Этот же модуль импортируется основным приложением, чтобы
ставить задачи в очередь (`parse_url_task.delay(url)`).
"""
import asyncio

from celery import Celery
from celery.schedules import crontab

from app.config import settings
from app.parsing import parse_and_save_async

celery = Celery(
    "lr3",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)
# Псевдоним, чтобы `celery -A worker.celery_app` гарантированно нашёл инстанс.
app = celery

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
)


@celery.task(name="parse_url_task", bind=True, max_retries=2, default_retry_delay=5)
def parse_url_task(self, url: str) -> dict:
    """Фоновая задача: парсит URL и асинхронно сохраняет заголовок в БД.

    Тело задачи в Celery синхронное, поэтому асинхронную запись запускаем через
    asyncio.run — сам commit внутри выполняется неблокирующе (await).
    """
    try:
        return asyncio.run(parse_and_save_async(url, source="celery"))
    except Exception as exc:
        # Повторяем задачу при временной ошибке (например, сеть недоступна).
        raise self.retry(exc=exc)


@celery.task(name="count_parsed_pages_task")
def count_parsed_pages_task() -> int:
    """Периодическая задача: считает число распарсенных страниц в БД."""
    from app.database import SessionLocal
    from app.models import ParsedPage

    session = SessionLocal()
    try:
        count = session.query(ParsedPage).count()
        print(f"[periodic] всего распарсено страниц: {count}")
        return count
    finally:
        session.close()


# --- Периодические задачи (bonus): запуск count_parsed_pages_task раз в минуту ---
celery.conf.beat_schedule = {
    "count-parsed-pages-every-minute": {
        "task": "count_parsed_pages_task",
        "schedule": crontab(minute="*"),  # каждую минуту
    },
}


@celery.on_after_configure.connect
def _ensure_tables(sender, **kwargs):
    """Гарантируем наличие таблиц при старте воркера."""
    try:
        from app.init_db import init_db
        init_db()
    except Exception as e:  # не валим воркер, если БД ещё не готова
        print(f"[worker] init_db отложен: {e}")
