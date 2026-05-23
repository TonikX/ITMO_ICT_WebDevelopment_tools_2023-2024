import asyncio
import time

N = 1_000_000
WORKERS = 4


def calculate_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))


async def run_async(workers: int = WORKERS) -> dict:
    chunk = N // workers
    tasks = []
    started = time.perf_counter()
    for index in range(workers):
        left = index * chunk + 1
        right = N if index == workers - 1 else (index + 1) * chunk
        tasks.append(asyncio.to_thread(calculate_sum, left, right))
    parts = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - started

    total = sum(parts)
    return {"mode": "async", "workers": workers, "result": total, "elapsed_sec": elapsed}


def run(workers: int = WORKERS) -> dict:
    return asyncio.run(run_async(workers))


if __name__ == "__main__":
    output = run()
    print(output)
