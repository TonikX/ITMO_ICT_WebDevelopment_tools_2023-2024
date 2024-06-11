import asyncio
import time

async def calculate_sum(start, end):
    return sum(range(start, end))

async def main():
    task1 = asyncio.create_task(calculate_sum(1, 500001))
    task2 = asyncio.create_task(calculate_sum(500001, 1000001))

    start_time = time.time()

    result1 = await task1
    result2 = await task2

    total_sum = result1 + result2

    end_time = time.time()
    execution_time = end_time - start_time

    print("Total sum using async:", total_sum)
    print("Execution time:", execution_time, "seconds")

if __name__ == "__main__":
    asyncio.run(main())
