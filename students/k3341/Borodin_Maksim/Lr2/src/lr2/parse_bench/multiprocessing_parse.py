import multiprocessing as mp
import time

import requests

from lr2.common.db import ensure_parsed_pages_table
from lr2.common.http_utils import extract_title
from lr2.common.storage import save_parsed_page
from lr2.parse_bench.urls import URLS


def parse_and_save(url: str) -> dict:
    started = time.perf_counter()
    title = None
    status = "failed"
    http_status_code = None
    error_message = None
    try:
        response = requests.get(url, timeout=15)
        http_status_code = response.status_code
        response.raise_for_status()
        title = extract_title(response.text)
        status = "success"
    except Exception as exc:
        error_message = str(exc)[:500]
    duration_ms = int((time.perf_counter() - started) * 1000)
    save_parsed_page(
        url=url,
        title=title,
        status=status,
        concurrency_mode="multiprocessing",
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


def run(urls: list[str] | None = None, workers: int = 4) -> dict:
    ensure_parsed_pages_table()
    target_urls = urls or URLS
    started = time.perf_counter()
    with mp.Pool(processes=min(workers, len(target_urls))) as pool:
        results = pool.map(parse_and_save, target_urls)
    elapsed = time.perf_counter() - started
    for item in results:
        print(f"[multiprocessing] {item['url']} -> {item['status']} ({item['duration_ms']}ms)")
    return {"mode": "multiprocessing", "elapsed_sec": elapsed, "results": results}


if __name__ == "__main__":
    print(run())
