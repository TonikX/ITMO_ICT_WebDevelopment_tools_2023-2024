import asyncio
from time import time


async def calculate_sum(start, end, index):
    s = sum(range(start, end + 1))
    return s


async def main():
    start_time = time()
    task_count = 5
    numbers_per_task = 1_000_000 // task_count
    tasks = list()

    for i in range(task_count):
        start = i * numbers_per_task + 1
        end = start + numbers_per_task - 1
        tasks.append(calculate_sum(start, end))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    end_time = time()

    print(f"Сумма: {total_sum}")
    print(f"Время выполнения: {end_time - start_time}")


if __name__ == "__main__":
    asyncio.run(main())

