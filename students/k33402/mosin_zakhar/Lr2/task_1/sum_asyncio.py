import asyncio


async def calculate_sum(start, end):
    return sum(range(start, end))


async def main():
    chunk_size = 100000
    tasks = []
    num = 1_000_000
    for i in range(0, num, chunk_size):
        tasks.append(calculate_sum(i+1, i+chunk_size+1))

    partial_sums = await asyncio.gather(*tasks)
    total_sum = sum(partial_sums)
    print("Result:", total_sum)

if __name__ == "__main__":
    print("ASYNCIO")
    import time
    start_time = time.time()
    asyncio.run(main())
    print("Time:", time.time() - start_time)
