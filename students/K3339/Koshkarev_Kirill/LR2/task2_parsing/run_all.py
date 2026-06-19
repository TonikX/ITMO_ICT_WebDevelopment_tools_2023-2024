"""Запускает все три подхода задачи 2 + последовательный базовый вариант
и печатает сравнительную таблицу времени.

Использование:
    python run_all.py
"""
import time

from db import count_pages, init_db, save_page
from urls import URLS, extract_title, fetch_sync

import threading_parse
import multiprocessing_parse
import async_parse


def sequential():
    """Базовый последовательный парсинг — для сравнения."""
    init_db()
    start = time.perf_counter()
    for url in URLS:
        try:
            html = fetch_sync(url)
            title = extract_title(html)
            page_id = save_page(url, title, "sequential")
            print(f"  [#{page_id}] {url}\n        -> {title}")
        except Exception as e:
            print(f"  [ERR] {url}: {type(e).__name__}: {e}")
    elapsed = time.perf_counter() - start
    print(f"[sequential] распарсено {len(URLS)} страниц за {elapsed:.3f} c")
    return elapsed


def main():
    print("=" * 64)
    print(f"Задача 2. Параллельный парсинг {len(URLS)} страниц")
    print("=" * 64)

    print("\n--- sequential ---")
    t_seq = sequential()
    print("\n--- threading ---")
    t_thread = threading_parse.run()
    print("\n--- async ---")
    t_async = async_parse.run()
    print("\n--- multiprocessing ---")
    t_proc = multiprocessing_parse.run()

    print("\n" + "=" * 64)
    print(f"Всего записей в таблице parsed_pages: {count_pages()}")
    print("=" * 64)

    rows = [
        ("sequential", t_seq),
        ("threading", t_thread),
        ("multiprocessing", t_proc),
        ("async", t_async),
    ]
    print(f"{'Подход':<18}{'Время, c':>12}{'Ускорение':>14}")
    print("-" * 44)
    for name, t in rows:
        speedup = t_seq / t if t > 0 else float("inf")
        print(f"{name:<18}{t:>12.3f}{speedup:>13.2f}x")


if __name__ == "__main__":
    main()
