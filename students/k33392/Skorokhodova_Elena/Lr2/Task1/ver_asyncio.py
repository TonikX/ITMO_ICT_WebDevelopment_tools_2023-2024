import asyncio
import time


async def calculate_sum(start, end):
    return sum(range(start, end))


async def main():
    start_time = time.time()
    task1 = asyncio.create_task(calculate_sum(1, 500001))
    task2 = asyncio.create_task(calculate_sum(500001, 1000001))

    result1, result2 = await asyncio.gather(task1, task2)

    total_sum = result1 + result2
    end_time = time.time()
    print("Total sum using asyncio:", total_sum)
    print("Time taken:", end_time - start_time, "seconds")


if __name__ == "__main__":
    asyncio.run(main())
