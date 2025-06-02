import time
import asyncio

N = 1_000_000_000
NUM_TASKS = 4

async def partial_sum_async(start: int, end: int) -> int:
    total = 0
    chunk = 1_000_000
    count = start
    while count <= end:
        upper = min(end, count + chunk - 1)
        for i in range(count, upper + 1):
            total += i
        count = upper + 1
        await asyncio.sleep(0)
    return total

async def main():
    chunk_size = N // NUM_TASKS
    tasks = []
    for i in range(NUM_TASKS):
        start = i * chunk_size + 1
        end = N if i == NUM_TASKS - 1 else (i + 1) * chunk_size
        tasks.append(asyncio.create_task(partial_sum_async(start, end)))
    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    return total_sum

if __name__ == "__main__":
    start_time = time.time()
    total_sum = asyncio.run(main())
    elapsed = time.time() - start_time
    print(f"Total sum = {total_sum}")
    print(f"Completed in {elapsed:.2f} seconds")
