import asyncio
from time import time


async def calculate_sum(start, end):
    total_sum = sum(range(start, end + 1))
    return total_sum


async def main():
    n_coroutines = 4
    numbers_per_coroutine = 1000000 // n_coroutines
    tasks = []

    start_time = time()

    for i in range(n_coroutines):
        start = i * numbers_per_coroutine + 1
        end = (i + 1) * numbers_per_coroutine if i != n_coroutines - 1 else 1000000
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    print(f"Total Sum: {total_sum}")
    print(f"Async time: {time() - start_time:.2f}")


if __name__ == "__main__":
    asyncio.run(main())