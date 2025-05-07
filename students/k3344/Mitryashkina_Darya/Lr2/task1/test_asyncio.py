import asyncio
import time

async def calculate_sum(start, end):
    print(f"Calculating: start {start}, end {end}")
    total = 0
    for i in range(start, end):
        total += i
    return total

async def main():    
    N = 10**9
    num_threads = 10

    tasks = []

    for i in range(num_threads):
        start = i * N // num_threads
        end = (i + 1) * N // num_threads
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    total_sum = sum(results) + N
    print("Total sum:", total_sum)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")


# Total sum: 500000000500000000
# Time taken: 48.17 seconds