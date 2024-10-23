import asyncio
import time


async def calculate_sum(start, stop):
    summary = 0
    for i in range(start, stop):
        summary += i
    return summary


async def main():
    tasks = [asyncio.create_task(calculate_sum(i, i + 10**4)) for i in range(1, 10**9, 10**4)]

    for task in tasks:
        await task

    return sum(task.result() for task in tasks)


time_start = time.time()
print(asyncio.run(main()))
print(time.time() - time_start)
# Время выполнения: 0.02916574478149414
# Время выполнения: 39.74562740325928
