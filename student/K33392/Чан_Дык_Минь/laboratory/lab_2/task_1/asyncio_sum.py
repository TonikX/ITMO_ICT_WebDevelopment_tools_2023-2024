import asyncio
import time

NUM_TASKS = 10
NUMBERS = 1000000

async def calculate_sum(start, end):
    partial_sum = sum(range(start, end))
    return partial_sum

async def get_range(i, chunk_size):
    start = i * chunk_size + 1
    end = start + chunk_size
    return start, end

async def main():
    chunk_size = NUMBERS // NUM_TASKS
    tasks = []

    for i in range(NUM_TASKS):
        start, end = await get_range(i, chunk_size)
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    final_sum = sum(results)

    print("Sum of first 1000000 numbers using Asyncio:", final_sum)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print("Execution time using Asyncio:", time.time() - start_time)