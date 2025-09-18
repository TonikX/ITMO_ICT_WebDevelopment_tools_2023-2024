import asyncio
import time


async def calculate_sum(start, end):
    """Асинхронно вычисляет сумму чисел от start до end"""
    partial_sum = 0
    for num in range(start, end + 1):
        partial_sum += num
    return partial_sum


async def async_sum(N, num_tasks=4):
    """Основная асинхронная функция для вычисления суммы"""
    chunk_size = N // num_tasks
    tasks = []

    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_tasks - 1 else N
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total = sum(results)
    
    return total


async def main():
    N = 1_000_000_000
    num_tasks = 4
    print(f"Calculating sum from 1 to {N:,}")

    start_time = time.time()
    total = await async_sum(N, num_tasks)
    end_time = time.time()
    duration = end_time - start_time
        
    print(f"Async sum: {total}")
    print(f"Time: {duration:.4f} seconds")
    print(f"Tasks used: {num_tasks}")


if __name__ == "__main__":
    asyncio.run(main())