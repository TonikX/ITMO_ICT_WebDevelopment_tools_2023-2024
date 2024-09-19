import asyncio
import time


async def sum_numbers(start, end):
    return sum(range(start, end))


async def calculate_sum():
    tasks_num = 4
    numbers_per_task = 1000000 // tasks_num

    tasks = [sum_numbers(i * numbers_per_task + 1, (i + 1) * numbers_per_task + 1) for i in range(tasks_num)]

    partial_sums = await asyncio.gather(*tasks)

    total_sum = sum(partial_sums)
    print("Total sum is", total_sum)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(calculate_sum())
    elapsed_time = time.time() - start_time
    print("Elapsed time:", elapsed_time)
