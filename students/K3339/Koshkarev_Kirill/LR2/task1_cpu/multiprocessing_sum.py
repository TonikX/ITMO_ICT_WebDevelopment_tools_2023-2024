"""Задача 1 — подход MULTIPROCESSING.

Сумма 1..N считается несколькими ПРОЦЕССАМИ (multiprocessing). Каждый процесс
имеет собственный интерпретатор Python и собственный GIL, поэтому процессы
выполняются по-настоящему параллельно на разных ядрах CPU.

Особенность: для CPU-bound задач это даёт реальное ускорение (близко к числу
ядер). Платой являются накладные расходы на создание процессов и передачу
данных между ними (сериализация через pickle).
"""
import time
from multiprocessing import Pool

from common import expected_sum, make_ranges, parse_args, partial_sum


def _worker(args):
    start, end = args
    return partial_sum(start, end)


def calculate_sum(n: int, workers: int) -> int:
    ranges = make_ranges(n, workers)
    with Pool(processes=workers) as pool:
        results = pool.map(_worker, ranges)
    return sum(results)


def run(n: int, workers: int):
    start = time.perf_counter()
    total = calculate_sum(n, workers)
    elapsed = time.perf_counter() - start

    assert total == expected_sum(n), "Неверный результат!"
    print(f"[multiprocessing] N={n:,} workers={workers}")
    print(f"  сумма = {total}")
    print(f"  время = {elapsed:.3f} c")
    return elapsed


if __name__ == "__main__":
    n, workers = parse_args()
    run(n, workers)
