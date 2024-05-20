import asyncio
import time


async def calculate_sum(start, end):
    return sum(range(start, end))

async def main():
    start = 1
    end = 1000000
    n_tasks = 4
    step = int(end / n_tasks)

    tasks = []
    for i in range(n_tasks):
        step_start = i * step + start
        step_end = (i + 1) * step + start if i != n_tasks - 1 else end + 1
        task = asyncio.create_task(calculate_sum(step_start, step_end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    print("Total sum:", total_sum)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")