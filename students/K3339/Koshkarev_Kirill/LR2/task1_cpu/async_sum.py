"""Задача 1 — подход ASYNC (asyncio).

Сумма 1..N разбивается на подзадачи-корутины, которые запускаются через
asyncio.gather.

Особенность: asyncio — это КООПЕРАТИВНАЯ многозадачность в ОДНОМ потоке. Реальный
параллелизм возможен только в точках await, где корутина уступает управление
(обычно при ожидании I/O). Для чисто вычислительной (CPU-bound) задачи точек
ожидания нет, поэтому корутины выполняются фактически последовательно —
ускорения по сравнению с однопоточным кодом нет. Это показывает, что asyncio
предназначен для I/O-bound, а не CPU-bound нагрузок (см. задачу 2).
"""
import asyncio
import time

from common import expected_sum, make_ranges, parse_args, partial_sum


async def _worker(start: int, end: int) -> int:
    # Внутри нет await на I/O — вычисление монополизирует поток до конца.
    return partial_sum(start, end)


async def calculate_sum(n: int, workers: int) -> int:
    ranges = make_ranges(n, workers)
    results = await asyncio.gather(*(_worker(start, end) for start, end in ranges))
    return sum(results)


def run(n: int, workers: int):
    start = time.perf_counter()
    total = asyncio.run(calculate_sum(n, workers))
    elapsed = time.perf_counter() - start

    assert total == expected_sum(n), "Неверный результат!"
    print(f"[async]          N={n:,} workers={workers}")
    print(f"  сумма = {total}")
    print(f"  время = {elapsed:.3f} c")
    return elapsed


if __name__ == "__main__":
    n, workers = parse_args()
    run(n, workers)
