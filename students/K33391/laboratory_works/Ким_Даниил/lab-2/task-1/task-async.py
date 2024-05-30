import asyncio
import time


async def calculate_sum(start, end):
    return sum(range(start, end))


async def worker(start, end, results, index):
    results[index] = await calculate_sum(start, end)


async def main():
    num_tasks = 4
    n = 1000000
    step = n // num_tasks
    tasks = []
    results = [0] * num_tasks

    start_time = time.time()
    for i in range(num_tasks):
        start = i * step + 1
        end = (i + 1) * step + 1
        task = asyncio.create_task(worker(start, end, results, i))
        tasks.append(task)

    await asyncio.gather(*tasks)

    total_sum = sum(results)
    end_time = time.time()
    print(f"Total sum is {total_sum}, computed in {end_time - start_time} seconds")


if __name__ == "__main__":
    asyncio.run(main())
