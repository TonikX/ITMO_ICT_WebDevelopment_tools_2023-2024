import asyncio
import time

async def calculate_partial_sum(start, end):
    return sum(range(start, end + 1))

async def calculate_sum():
    total_tasks = 4
    n = 1000000
    step = n // total_tasks
    tasks = []

    for i in range(total_tasks):
        start = i * step + 1
        end = (i + 1) * step if i != total_tasks - 1 else n
        tasks.append(asyncio.create_task(calculate_partial_sum(start, end)))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    return total_sum

start_time = time.time()
sum_result = asyncio.run(calculate_sum())
end_time = time.time()
print(f"Async sum: {sum_result}, Time taken: {end_time - start_time} seconds")