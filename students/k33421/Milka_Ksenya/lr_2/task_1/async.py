import asyncio
import time


async def calculate_sum(start, end):
    return sum(range(start, end))


async def main(tasks_count, start, end):
    tasks = []

    for i in range(tasks_count):
        tasks.append(
            asyncio.create_task(
                calculate_sum(
                    start + i * (end - start + 1) // tasks_count,
                    start + (i + 1) * (end - start + 1) // tasks_count
                )
            )
        )

    start_time = time.perf_counter()
    result = sum(await asyncio.gather(*tasks))
    end_time = time.perf_counter()

    print(f'Время выполнения: {end_time - start_time:.3f} секунд')

    return result


if __name__ == '__main__':
    asyncio.run(
        main(
            tasks_count=10,
            start=1,
            end=1_000_000
        )
    )