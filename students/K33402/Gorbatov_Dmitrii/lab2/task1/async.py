import asyncio
import time

def calculate_sum(start, finish, result_list, index):
    total = 0
    for i in range(start, finish + 1):
        total += i
    result_list[index] = total

async def async_calculate_sum(start, end, result_list, index):
    calculate_sum(start, end, result_list, index)

async def asyncio_example():
    tasks = []
    chunks = 5
    total = 1000000
    chunk_size = total // chunks
    results = [0] * chunks

    start_time = time.time()
    for i in range(chunks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        task = asyncio.create_task(async_calculate_sum(start, end, results, i))
        tasks.append(task)

    await asyncio.gather(*tasks)
    end_time = time.time()

    final_result = sum(results)
    print(f"Result: {final_result}")
    print(f"Asyncio time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(asyncio_example())
