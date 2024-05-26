import multiprocessing
from Lr2.mark_time import mark_time


def calculate_part_sum(start, end):
    s = 0
    for i in range(start, end + 1):
        s += i
    return s


@mark_time
def calculate_sum(n=1000000, n_processes=4):
    with multiprocessing.Pool(n_processes) as pool:
        step = n // n_processes
        ranges = [
            (i * step + 1, n)
            if i == n_processes - 1
            else (i * step + 1, (i + 1) * step)
            for i in range(n_processes)
        ]
        # Задачи распределяются между процессами и считаются частичные суммы
        results = pool.starmap(calculate_part_sum, ranges)
    return sum(results)


if __name__ == "__main__":
    print(calculate_sum())
