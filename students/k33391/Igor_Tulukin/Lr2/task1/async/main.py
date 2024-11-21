import asyncio
import time

async def calculate_sum(start, end):
    return sum(range(start, end))

async def main():
    start_time = time.time()

    tasks = []
    ranges = [(1, 250000), (250001, 500000), (500001, 750000), (750001, 1000001)]

    for start, end in ranges:
        tasks.append(calculate_sum(start, end))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    end_time = time.time()

    print(f"Async/Await Sum: {total_sum}, Time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
