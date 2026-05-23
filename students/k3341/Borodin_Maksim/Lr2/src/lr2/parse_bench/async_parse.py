import asyncio
import time

import aiohttp

from lr2.common.db import ensure_parsed_pages_table
from lr2.common.http_utils import extract_title
from lr2.common.storage import save_parsed_page
from lr2.parse_bench.urls import URLS


async def parse_and_save(session: aiohttp.ClientSession, url: str) -> dict:
    started = time.perf_counter()
    title = None
    status = "failed"
    http_status_code = None
    error_message = None
    try:
        async with session.get(url, timeout=15) as response:
            http_status_code = response.status
            response.raise_for_status()
            text = await response.text()
            title = extract_title(text)
            status = "success"
    except Exception as exc:
        error_message = str(exc)[:500]
    duration_ms = int((time.perf_counter() - started) * 1000)
    await asyncio.to_thread(
        save_parsed_page,
        url=url,
        title=title,
        status=status,
        concurrency_mode="async",
        http_status_code=http_status_code,
        error_message=error_message,
        duration_ms=duration_ms,
    )
    return {
        "url": url,
        "title": title,
        "status": status,
        "http_status_code": http_status_code,
        "duration_ms": duration_ms,
    }


async def run_async(urls: list[str] | None = None) -> dict:
    ensure_parsed_pages_table()
    target_urls = urls or URLS
    started = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in target_urls]
        results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - started
    for item in results:
        print(f"[async] {item['url']} -> {item['status']} ({item['duration_ms']}ms)")
    return {"mode": "async", "elapsed_sec": elapsed, "results": results}


def run(urls: list[str] | None = None) -> dict:
    return asyncio.run(run_async(urls))


if __name__ == "__main__":
    print(run())
