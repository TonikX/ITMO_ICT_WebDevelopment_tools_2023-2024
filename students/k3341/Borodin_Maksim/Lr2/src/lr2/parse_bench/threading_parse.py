import threading
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
        concurrency_mode="threading",
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


def run(urls: list[str] | None = None) -> dict:
    ensure_parsed_pages_table()
    target_urls = urls or URLS
    results: list[dict] = [None] * len(target_urls)  # type: ignore
    threads: list[threading.Thread] = []
    started = time.perf_counter()

    def worker(index: int, url: str) -> None:
        results[index] = parse_and_save(url)
        print(f"[threading] {url} -> {results[index]['status']} ({results[index]['duration_ms']}ms)")

    for index, url in enumerate(target_urls):
        thread = threading.Thread(target=worker, args=(index, url))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    elapsed = time.perf_counter() - started
    return {"mode": "threading", "elapsed_sec": elapsed, "results": results}


if __name__ == "__main__":
    print(run())
