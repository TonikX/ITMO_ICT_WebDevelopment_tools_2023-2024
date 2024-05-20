import asyncio
import time


async def calculate_sum(start, end):
    total = sum(range(start, end + 1))
    return total


async def main():
    n_tasks = 4
    tasks = []
    chunk_size = 1000000 // n_tasks

    for i in range(n_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != n_tasks - 1 else 1000000
        tasks.append(calculate_sum(start, end))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    print(f"Total sum: {total_sum}")

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
