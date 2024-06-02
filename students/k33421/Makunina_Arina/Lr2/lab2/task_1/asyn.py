import asyncio
from time import time


async def calculate_sum(start, end):
    total = sum(range(start, end + 1))
    return total


async def main():
    task_count = 10
    numbers_per_task = 100000 // task_count
    tasks = []

    start_time = time()
    for i in range(task_count):
        start = i * numbers_per_task + 1
        end = start + numbers_per_task - 1
        tasks.append(calculate_sum(start, end))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    print(f"Total sum is {total_sum}")

    end_time = time()
    print(f"Async time: {end_time - start_time}")


if __name__ == "__main__":
    asyncio.run(main())
