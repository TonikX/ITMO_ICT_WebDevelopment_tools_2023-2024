import asyncio
import time

import aiohttp

from task_2.db import insert_user_data
from task_2.parse import extract_user_data

BASE_URL = 'https://moihottur.ru/companion/'
PAGINATION_KEY = 'page'
PAGES = 10


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_and_save(url):
    page = await fetch(url)
    user_data = extract_user_data(page)
    insert_user_data(user_data)


async def main():
    tasks = [
        asyncio.create_task(parse_and_save(f'{BASE_URL}?{PAGINATION_KEY}={i}'))
        for i in range(1, PAGES + 1)
    ]

    start_time = time.perf_counter()
    await asyncio.gather(*tasks)
    end_time = time.perf_counter()

    print(f'Finished in {end_time - start_time:.3f} seconds')


if __name__ == '__main__':
    asyncio.run(main())
