"""Запускает все три подхода задачи 1 и печатает сравнительную таблицу времени.

Использование:
    python run_all.py [N] [workers]
Например:
    python run_all.py 100000000 8
"""
import time

from common import expected_sum, make_ranges, parse_args, partial_sum

import threading_sum
import multiprocessing_sum
import async_sum
import asyncio


def sequential(n: int) -> float:
    """Базовая однопоточная реализация для сравнения."""
    start = time.perf_counter()
    total = partial_sum(1, n + 1)
    elapsed = time.perf_counter() - start
    assert total == expected_sum(n)
    print(f"[sequential]     N={n:,}")
    print(f"  сумма = {total}")
    print(f"  время = {elapsed:.3f} c")
    return elapsed


def main():
    n, workers = parse_args()
    print("=" * 60)
    print(f"Задача 1. Сумма чисел от 1 до {n:,} (workers={workers})")
    print("=" * 60)

    t_seq = sequential(n)
    print("-" * 60)
    t_thread = threading_sum.run(n, workers)
    print("-" * 60)
    t_async = async_sum.run(n, workers)
    print("-" * 60)
    t_proc = multiprocessing_sum.run(n, workers)
    print("=" * 60)

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
