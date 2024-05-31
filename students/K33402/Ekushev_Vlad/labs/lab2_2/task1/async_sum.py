import asyncio

TOTAL_NUMBERS = 1000000
TASK_COUNT = 10

async def compute_range_sum(start, end):
    return sum(range(start, end + 1))

async def run_tasks():
    tasks = []
    step = TOTAL_NUMBERS // TASK_COUNT

    for i in range(TASK_COUNT):
        range_start = i * step + 1
        range_end = (i + 1) * step
        tasks.append(compute_range_sum(range_start, range_end))

    results = await asyncio.gather(*tasks)
    final_sum = sum(results)
    print("Общая сумма с использованием async/await:", final_sum)

if __name__ == "__main__":
    import time

    start_time = time.time()
    asyncio.run(run_tasks())
    print("Время выполнения:", time.time() - start_time)

