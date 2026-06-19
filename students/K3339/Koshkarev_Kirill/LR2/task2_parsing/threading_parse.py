"""Задача 2 — параллельный парсинг через THREADING.

Каждую страницу обрабатывает отдельный поток. Сетевой запрос (I/O) — это как раз
тот случай, где потоки эффективны: во время ожидания ответа от сервера GIL
освобождается, и другие потоки могут работать. Поэтому для I/O-bound задач
threading даёт существенное ускорение.
"""
import threading
import time

from db import init_db, save_page
from urls import URLS, extract_title, fetch_sync

APPROACH = "threading"
_print_lock = threading.Lock()


def parse_and_save(url: str):
    """Загружает страницу, извлекает заголовок, сохраняет в БД и печатает."""
    try:
        html = fetch_sync(url)
        title = extract_title(html)
        page_id = save_page(url, title, APPROACH)
        with _print_lock:
            print(f"  [#{page_id}] {url}\n        -> {title}")
    except Exception as e:
        with _print_lock:
            print(f"  [ERR] {url}: {type(e).__name__}: {e}")


def run():
    init_db()
    start = time.perf_counter()
    threads = [threading.Thread(target=parse_and_save, args=(url,)) for url in URLS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start
    print(f"[threading] распарсено {len(URLS)} страниц за {elapsed:.3f} c")
    return elapsed


if __name__ == "__main__":
    run()
