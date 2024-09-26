import asyncio
import time


async def calculate_sum_async(start, end):
    return sum(range(start, end + 1))


async def main_async(total_numbers=1000000, ts=4):
    part = total_numbers // ts
    threads = []

    for i in range(ts):
        start = i * part + 1
        end = (i + 1) * part if i != ts-1 else total_numbers
        threads.append(calculate_sum_async(start, end))

    results = await asyncio.gather(*threads)
    total_sum = sum(results)
    print(f"Total sum is: {total_sum}")


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main_async())
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time} секунд")