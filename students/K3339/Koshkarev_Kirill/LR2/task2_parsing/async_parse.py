"""Задача 2 — параллельный парсинг через ASYNC (asyncio + aiohttp).

Все запросы выполняются в одном потоке, но «одновременно»: пока одна корутина
ждёт ответа сервера (await), управление переходит к другим. Для I/O-bound задач
это самый эффективный и лёгкий по ресурсам подход — нет ни накладных расходов на
процессы, ни ограничений GIL (он не мешает, т.к. время уходит на ожидание сети).

Запись в БД тоже асинхронная: используется SQLAlchemy async + драйвер aiosqlite,
поэтому commit выполняется через await и не блокирует событийный цикл (в отличие
от обёртки asyncio.to_thread вокруг синхронной записи).
"""
import asyncio
import time

import aiohttp

from db import async_save_page, init_db
from urls import URLS, extract_title

APPROACH = "async"


async def parse_and_save(session: aiohttp.ClientSession, url: str):
    """Асинхронно грузит страницу, парсит заголовок и сохраняет в БД."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
            html = await resp.text()
        title = extract_title(html)
        # Неблокирующая запись в БД через async-сессию.
        page_id = await async_save_page(url, title, APPROACH)
        print(f"  [#{page_id}] {url}\n        -> {title}")
    except Exception as e:
        print(f"  [ERR] {url}: {type(e).__name__}: {e}")


async def main():
    headers = {"User-Agent": "LR2-parser/1.0"}
    async with aiohttp.ClientSession(headers=headers) as session:
        await asyncio.gather(*(parse_and_save(session, url) for url in URLS))


def run():
    init_db()
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"[async] распарсено {len(URLS)} страниц за {elapsed:.3f} c")
    return elapsed


if __name__ == "__main__":
    run()
