import asyncio
from time import time


async def calc(offset, task_count):
    sum = 0
    for i in range(1 + offset, 1000001, task_count):
        sum += i
    return sum


async def main():
    task_count = 10
    tasks = []

    for i in range(task_count):
        tasks.append(calc(offset=i, task_count=task_count))

    results = await asyncio.gather(*tasks)
    print(sum(results))


if __name__ == "__main__":
    start_time = time()

    asyncio.run(main())

    end_time = time()
    print(end_time - start_time)