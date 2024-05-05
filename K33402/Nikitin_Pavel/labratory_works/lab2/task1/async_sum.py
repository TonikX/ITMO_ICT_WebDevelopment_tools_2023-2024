import asyncio

TOTAL = 1000000
NUM_TASKS = 10

async def calculate_sum(start, end):
    return sum(range(start, end+1))

async def main():
    tasks = []

    for i in range(NUM_TASKS):
        start = i * (TOTAL // NUM_TASKS) + 1
        end = (i + 1) * (TOTAL // NUM_TASKS)
        tasks.append(calculate_sum(start, end))

    partial_sums = await asyncio.gather(*tasks)
    total_sum = sum(partial_sums)
    print("Total sum using async/await:", total_sum)

if __name__ == "__main__":
    import time
    start_time = time.time()
    asyncio.run(main())
    print("Execution time:", time.time() - start_time)
