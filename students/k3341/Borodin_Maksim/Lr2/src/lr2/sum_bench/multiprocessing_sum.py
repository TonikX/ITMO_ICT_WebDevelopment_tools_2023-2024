import multiprocessing as mp
import time

N = 1_000_000
WORKERS = 4


def calculate_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))


def run(workers: int = WORKERS) -> dict:
    chunk = N // workers
    ranges: list[tuple[int, int]] = []
    for index in range(workers):
        left = index * chunk + 1
        right = N if index == workers - 1 else (index + 1) * chunk
        ranges.append((left, right))

    started = time.perf_counter()
    with mp.Pool(processes=workers) as pool:
        parts = pool.starmap(calculate_sum, ranges)
    elapsed = time.perf_counter() - started

    total = sum(parts)
    return {
        "mode": "multiprocessing",
        "workers": workers,
        "result": total,
        "elapsed_sec": elapsed,
    }


if __name__ == "__main__":
    output = run()
    print(output)
