import asyncio
import time

start_time = time.time()
async def calculate_sum(start, end):
    total = sum(range(start, end))
    return total

async def main():
    tasks = []
    num_tasks = 4
    chunk_size = 1000000 // num_tasks
    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    print("Total sum using async/await:", total_sum)

asyncio.run(main())

end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения программы: {execution_time} секунд")