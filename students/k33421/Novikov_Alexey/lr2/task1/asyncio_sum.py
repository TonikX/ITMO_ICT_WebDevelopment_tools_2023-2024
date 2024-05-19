import asyncio
import time


async def calculate_partial_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))


async def calculate_sum() -> None:
    start_time = time.time()

    tasks = [
        asyncio.create_task(calculate_partial_sum(1, 250000)),
        asyncio.create_task(calculate_partial_sum(250001, 500000)),
        asyncio.create_task(calculate_partial_sum(500001, 750000)),
        asyncio.create_task(calculate_partial_sum(750001, 1000000)),
    ]

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)

    print(
        f"Сумма: {total_sum}\n"
        f"Время: {time.time() - start_time}"
    )


if __name__ == "__main__":
    asyncio.run(calculate_sum())
