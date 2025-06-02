from __future__ import annotations

import asyncio
import json
import os
from typing import Any, Dict

import redis.asyncio as aioredis

from parser import fetch_html_and_title

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
            payload: Dict[str, Any] = json.loads(raw)
            req_id = payload["id"]
            url = payload["url"]
            print(f"[listener] got task id={req_id} url={url}")

            try:
                title, html = await fetch_html_and_title(url)
                result = {"status": "success", "title": title, "html": html}
            except Exception as err:  # noqa: BLE001
                print("[listener] task failed", err)
                result = {"status": "failure", "error": str(err)}

            await redis.set(f"{RESULT_PREFIX}{req_id}", json.dumps(result), ex=3600)
            print(f"[listener] stored result for id={req_id}")
        except Exception as exc:  # noqa: BLE001
            print("[listener] error:", exc)
            await asyncio.sleep(1)