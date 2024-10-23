from parser import parse
import asyncio
import time


async def main():
    tasks = []

    for season_start, year in zip(range(226, 241, 5), range(2008, 2024, 5)):
        tasks.append(asyncio.create_task(parse(season_start, season_start + 4, year)))
    time.sleep(15)

    for task in tasks:
        await task


time_start = time.time()
asyncio.run(main())
print(time.time() - time_start)
# 497.043781042099
