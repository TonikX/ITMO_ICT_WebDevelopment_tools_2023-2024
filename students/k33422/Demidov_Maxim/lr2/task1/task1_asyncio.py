import asyncio


async def calculate_sum(start, end):
    return sum(range(start, end))


async def main():
    num_tasks = 4
    chunk_size = 1000000 // num_tasks
    tasks = []

    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    partial_sums = await asyncio.gather(*tasks)
    total_sum = sum(partial_sums)
    print("Total sum:", total_sum)


if __name__ == "__main__":
    import time

    start_time = time.time()
    asyncio.run(main())
    print("Execution time:", time.time() - start_time)
