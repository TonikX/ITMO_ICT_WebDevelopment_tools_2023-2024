import asyncio
import time


async def calculate_sum(start, end):
    return sum(range(start, end))


async def calculate():
    tasks = []

    for i in range(20):
        start = i * 50000 + 1
        end = (i + 1) * 50000 + 1
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    total_sum = sum(await asyncio.gather(*tasks))
    print("Total sum:", total_sum)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(calculate())
    print(f"Async time: {time.time() - start_time}")
