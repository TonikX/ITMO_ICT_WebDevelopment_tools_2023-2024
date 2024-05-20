import asyncio
from time import time

async def calculate_sum(start, end):
    return sum(range(start, end + 1))

async def main():
    tasks = []
    num_tasks = 10
    total_numbers = 1000000
    chunk_size = total_numbers // num_tasks
    start_time = time()

    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_tasks - 1 else total_numbers
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    
    print(f"Total Sum: {total_sum}")
    print(f"Time taken: {time() - start_time}")

if __name__ == "__main__":
    asyncio.run(main())
