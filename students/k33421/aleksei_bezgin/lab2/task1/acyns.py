import asyncio
import time

async def calculate_sum(start, end):
    result = sum(range(start, end))
    print(f"sum from {start} to {end}: {result}")

async def main(num_of_tasks=5, step=1000000):
    start_time = time.time()
    tasks = []
    for i in range(num_of_tasks):
        task = asyncio.create_task(calculate_sum(i*step+1, (i+1)*step))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    print(f"execution time: {round(time.time() - start_time, 5)} seconds")

if __name__ == "__main__":
    num_of_tasks = 10
    step = 10000000
    asyncio.run(main(num_of_tasks, step))