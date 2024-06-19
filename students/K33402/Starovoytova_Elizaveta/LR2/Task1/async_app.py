import asyncio
import time


async def calculate_partial_sum(start, end):
    partial_sum = sum(range(start, end))
    return partial_sum


async def calculate_sum():
    num_tasks = 5
    chunk_size = 1000000 // num_tasks

    tasks = []
    start_time = time.time()
    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1 if i < num_tasks - 1 else 1000001
        task = asyncio.create_task(calculate_partial_sum(start, end))
        tasks.append(task)

    partial_sums = await asyncio.gather(*tasks)
    total_sum = sum(partial_sums)

    end_time = time.time()
    print("Total sum (Async):", total_sum)
    print("Time taken:", end_time - start_time, "seconds")


if __name__ == "__main__":
    asyncio.run(calculate_sum())
