import asyncio
import time

START = 1
END = 1_000_000_00
TASKS = 10
STEP = (END - START + 1) // TASKS


async def calculate_sum(start, end):
    return sum(range(start, end))


async def main():
    tasks = [
        asyncio.create_task(
            calculate_sum(
                START + i * STEP,
                START + (i + 1) * STEP
            )
        )
        for i in range(TASKS)
    ]

    start_time = time.perf_counter()
    results = await asyncio.gather(*tasks)
    result = sum(results)
    end_time = time.perf_counter()

    print(f'Finished in {end_time - start_time:.3f} seconds')
    print(f'Result: {result}')


if __name__ == '__main__':
    asyncio.run(main())
