import asyncio

async def calculate_sum(start, end):
    return sum(range(start, end))

async def main():
    chunk_size = 100000
    tasks = []

    for i in range(0, 1000000, chunk_size):
        task = asyncio.create_task(calculate_sum(i+1, i+chunk_size+1))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    print("Sum:", sum(results))

if __name__ == "__main__":
    asyncio.run(main())

