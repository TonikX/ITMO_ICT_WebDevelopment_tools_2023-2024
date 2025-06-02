from __future__ import annotations

import asyncio
import json
import os
from time import time, sleep

import redis
from celery import shared_task
from sqlalchemy import select, update

from celery_app import celery_app
from database import AsyncSessionLocal, engine
from models import ParseRequest, StatusEnum

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
TASK_QUEUE = os.getenv("TASK_QUEUE", "parser:tasks")
RESULT_PREFIX = os.getenv("RESULT_PREFIX", "parser:results:")


@shared_task(name="api.parse_url", queue="api")
def parse_url_task(request_id: int, url: str) -> None:
    """Кладёт задание в Redis, ждёт результат, затем пишет его в БД."""
    r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

    # 1) Отправляем задачу парсеру
    payload = json.dumps({"id": request_id, "url": url})
    r.lpush(TASK_QUEUE, payload)

    # 2) Блокирующе ждём результат (макс 30 c)
    res_key = f"{RESULT_PREFIX}{request_id}"
    deadline = time() + 30
    result_data: dict[str, str] | None = None
    while time() < deadline:
        data = r.get(res_key)
        if data:
            result_data = json.loads(data)
            r.delete(res_key)
            break
        sleep(1)  # Redis >= 5 client helper

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
        asyncio.run(_write(StatusEnum.failure, title=None, html="Timeout waiting result"))
        return

    if result_data.get("status") == "success":
        asyncio.run(_write(StatusEnum.success, result_data.get("title"), result_data.get("html")))
    else:
        asyncio.run(_write(StatusEnum.failure, html=result_data.get("error")))