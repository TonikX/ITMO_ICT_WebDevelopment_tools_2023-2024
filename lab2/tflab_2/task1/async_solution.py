import asyncio
import time

async def calculate_sum(start, end):
    return sum(range(start, end))

async def main():
    target = 1000000000
    num_tasks = 5
    chunk_size = target // num_tasks
    tasks = []

    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1
        tasks.append(calculate_sum(start, end))

    start_time = time.time()
    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    print(f"Количество задач: {num_tasks}")
    print(f"Счёт до {target}")
    print(f"Общая сумма: {total_sum}")
    print(f"Время выполнения при помощи asyncio: {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    asyncio.run(main())
