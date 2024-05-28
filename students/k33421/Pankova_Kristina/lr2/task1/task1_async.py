import asyncio
import time

async def calculate_sum(start, end):
    total = 0
    for i in range(start, end+1):
        total += i
    return total

async def main():
    start_time = time.time()

    chunk_size = 10_000_000
    num_tasks = 4

    tasks = [asyncio.create_task(calculate_sum(i * chunk_size + 1, (i + 1) * chunk_size)) for i in range(num_tasks)]
    results = await asyncio.gather(*tasks)

    print(sum(results))

    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
