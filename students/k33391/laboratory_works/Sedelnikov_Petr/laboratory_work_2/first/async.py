import asyncio
import time


async def calculate_sum(start, end):
    return sum(range(start, end))


async def main():
    tasks_quantity = 4
    numbers = 1000000
    step = numbers // tasks_quantity
    tasks = []
    for i in range(tasks_quantity):
        start = i * step + 1
        end = (i + 1) * step + 1
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total = sum(results)
    print(f"Total: {total}")


if __name__ == "__main__":
    print("Async")
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
