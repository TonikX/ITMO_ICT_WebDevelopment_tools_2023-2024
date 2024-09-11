import asyncio
import time

from . import parse, database


async def iteration(page: int):
    content = await parse.async_get_content(page)

    data_list = parse.parse_data(content)

    for data in data_list:
        await database.async_insert_data_to_project(data)


async def main():
    tasks = [iteration(page) for page in range(1, 6)]
    start = time.perf_counter()
    await asyncio.gather(*tasks)
    end = time.perf_counter()
    print(f"Время: {end - start}")


asyncio.run(main())
