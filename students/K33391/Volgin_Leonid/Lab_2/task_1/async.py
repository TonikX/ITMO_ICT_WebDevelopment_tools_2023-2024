import asyncio
import time


async def calculate_sum(start, end):
    return sum(range(start, end))

async def main():
    tasks = 7
    total = 1000000
    step = total // tasks
    tasks_arr = []

    start = 1
    end = step + total % tasks + 1

    for i in range(tasks):
        task = asyncio.create_task(calculate_sum(start, end))
        start = end
        end = end + step
        tasks_arr.append(task)

    results = await asyncio.gather(*tasks_arr)
    total = sum(results)
    print(f"Total: {total}")


if __name__ == "__main__":
    print("Async")
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
    print("Гаусс справился бы быстрее")