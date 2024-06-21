import asyncio
import sys

async def calculate_partial_sum(start, end):
    return sum(range(start, end))

async def calculate_sum_async(num_tasks, total):
    step = total // num_tasks

    tasks = [calculate_partial_sum(i * step + 1, (i + 1) * step + 1) for i in range(num_tasks)]
    results = await asyncio.gather(*tasks)

    return sum(results)

if __name__ == "__main__":
    import time
    num_tasks = int(sys.argv[1])
    total = int(sys.argv[2])
    start_time = time.time()
    result = asyncio.run(calculate_sum_async(num_tasks, total))
    end_time = time.time()
    print(f"Async/await result: {result}, Time taken: {end_time - start_time} seconds")
