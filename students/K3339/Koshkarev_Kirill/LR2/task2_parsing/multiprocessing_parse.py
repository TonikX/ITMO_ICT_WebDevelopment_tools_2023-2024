"""Задача 2 — параллельный парсинг через MULTIPROCESSING.

Каждую страницу обрабатывает отдельный процесс из пула. Для I/O-bound задачи
процессы тоже дают ускорение (запросы идут одновременно), но по сравнению с
threading/async здесь выше накладные расходы: создание процессов, сериализация
и отдельное подключение к БД в каждом процессе. Для сетевого ввода-вывода это,
как правило, наименее выгодный из трёх подходов.
"""
import time
from multiprocessing import Pool

from db import init_db, save_page
from urls import URLS, extract_title, fetch_sync

APPROACH = "multiprocessing"


def parse_and_save(url: str) -> str:
    """Выполняется в отдельном процессе: грузит, парсит, пишет в БД."""
    try:
        html = fetch_sync(url)
        title = extract_title(html)
        page_id = save_page(url, title, APPROACH)
        result = f"  [#{page_id}] {url}\n        -> {title}"
    except Exception as e:
        result = f"  [ERR] {url}: {type(e).__name__}: {e}"
    print(result)
    return result


def run():
    init_db()
    start = time.perf_counter()
    with Pool(processes=min(len(URLS), 12)) as pool:
        pool.map(parse_and_save, URLS)
    elapsed = time.perf_counter() - start
    print(f"[multiprocessing] распарсено {len(URLS)} страниц за {elapsed:.3f} c")
    return elapsed


if __name__ == "__main__":
    run()
