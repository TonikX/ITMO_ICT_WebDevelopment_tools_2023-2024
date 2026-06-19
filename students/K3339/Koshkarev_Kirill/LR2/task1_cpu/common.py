"""Общие утилиты для задачи 1 (CPU-bound вычисление суммы).

Считаем сумму всех чисел от 1 до N. Формальная цель задания — N = 10**13,
однако «в лоб» обычным циклом Python это ~10^13 итераций (многие часы), поэтому
N вынесен в параметр командной строки. По умолчанию берётся 10**8 — этого
достаточно, чтобы наглядно увидеть разницу между подходами, и вычисление
завершается за разумное время. Поведение подходов от величины N не зависит.
"""
import sys

DEFAULT_N = 100_000_000  # 10**8
DEFAULT_WORKERS = 8


def partial_sum(start: int, end: int) -> int:
    """Сумма целых чисел в полуинтервале [start, end).

    Намеренно реализована обычным циклом, чтобы нагрузка была честно
    CPU-bound (а не свёрнута в формулу или C-уровневый sum()).
    """
    total = 0
    for i in range(start, end):
        total += i
    return total


def make_ranges(n: int, workers: int):
    """Разбивает диапазон [1, n] на `workers` примерно равных частей.

    Возвращает список пар (start, end) для полуинтервалов [start, end),
    покрывающих числа от 1 до n включительно.
    """
    ranges = []
    step = (n + workers - 1) // workers  # ceil
    start = 1
    while start <= n:
        end = min(start + step, n + 1)
        ranges.append((start, end))
        start = end
    return ranges


def expected_sum(n: int) -> int:
    """Эталон по формуле Гаусса: 1 + 2 + ... + n."""
    return n * (n + 1) // 2


def parse_args():
    """Простой разбор аргументов: N и число воркеров."""
    n = DEFAULT_N
    workers = DEFAULT_WORKERS
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    if len(sys.argv) > 2:
        workers = int(sys.argv[2])
    return n, workers
