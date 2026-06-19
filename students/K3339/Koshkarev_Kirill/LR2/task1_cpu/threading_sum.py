"""Задача 1 — подход THREADING.

Сумма 1..N считается несколькими потоками (threading.Thread). Каждый поток
обрабатывает свою часть диапазона.

Особенность: из-за GIL (Global Interpreter Lock) в CPython одновременно
выполняется только один поток с байт-кодом Python. Для CPU-bound задачи это
означает почти полное отсутствие ускорения (а иногда даже замедление из-за
накладных расходов на переключение потоков).
"""
import threading
import time

from common import expected_sum, make_ranges, parse_args, partial_sum


def calculate_sum(n: int, workers: int) -> int:
    ranges = make_ranges(n, workers)
    results = [0] * len(ranges)

    def worker(idx: int, start: int, end: int):
        results[idx] = partial_sum(start, end)

    threads = [
        threading.Thread(target=worker, args=(i, start, end))
        for i, (start, end) in enumerate(ranges)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return sum(results)


def run(n: int, workers: int):
    start = time.perf_counter()
    total = calculate_sum(n, workers)
    elapsed = time.perf_counter() - start

    assert total == expected_sum(n), "Неверный результат!"
    print(f"[threading]      N={n:,} workers={workers}")
    print(f"  сумма = {total}")
    print(f"  время = {elapsed:.3f} c")
    return elapsed


if __name__ == "__main__":
    n, workers = parse_args()
    run(n, workers)
