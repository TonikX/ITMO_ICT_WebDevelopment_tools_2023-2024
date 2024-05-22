import asyncio
from util import get_function_execution_time_sec_async


async def calculate_sum(start, end):
    total = 0
    for num in range(start, end + 1):
        total += num
    return total


async def main():
    num_tasks = 4
    start = 1
    end = 1000000
    step = int(end / num_tasks)

    tasks = []
    for i in range(num_tasks):
        task = asyncio.create_task(calculate_sum(start + i * step, start + (i + 1) * step - 1))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)

    print(f"Сумма чисел от 1 до 1000000: {total_sum}")


async def wrapper():
    time_sec, *_ = await get_function_execution_time_sec_async(main)
    print(f"Затраченное время - {time_sec:.3f} сек")


if __name__ == "__main__":
    asyncio.run(wrapper())
