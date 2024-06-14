import asyncio
from time import time


async def calculate_sum(start, end, index):
    print(f"started {index}")
    s = sum(range(start, end + 1))
    print(f"finished {index}")
    return s


async def main(task_count):
    numbers_per_task = 1_000_000 // task_count
    tasks = list()

    start_time = time()
    for i in range(task_count):
        start = i * numbers_per_task + 1
        end = start + numbers_per_task - 1
        tasks.append(calculate_sum(start, end, i))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    end_time = time()
    return total_sum, end_time - start_time


if __name__ == "__main__":
    result, time = asyncio.run(main(4))
    print(f"Result of execution 'async': {result}")
    print(f"Time of execution 'async': {time} seconds")

