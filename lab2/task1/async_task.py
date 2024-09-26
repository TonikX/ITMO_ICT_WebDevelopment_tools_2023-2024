import time
import asyncio

num = 5
number = 1000000


async def calculate_sum(start, end):
    return sum(range(start, end + 1))


async def Sum_asyncio():
    tasks = []
    chunk_size = number // num
    start_time = time.time()

    for i in range(num):
        start = i * chunk_size + 1
        end = start + chunk_size - 1
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    end_time = time.time()

    print(f"Сумма: {sum(results)}")
    print(f"Время: {end_time - start_time:.5f} секунд")


if __name__ == "__main__":
    asyncio.run(Sum_asyncio())
