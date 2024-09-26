import asyncio
import aiohttp
import time
import requests
from bs4 import BeautifulSoup
import asyncpg

from task_2.db import init_db
from models import *
from urls import URLS
import urllib.parse
QUERY = """INSERT INTO flat (size, cost) VALUES ($1, $2)"""


async def parse_and_save(url, db_pool):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                r = await response.text(encoding='utf-8', errors='ignore')
                soup = BeautifulSoup(r, 'html.parser')
                flats = soup.find_all('div', class_="catalog-block-item")
                for flat in flats:
                    try:
                        size = flat.find('div', class_='catalog-block-item-name').get_text().strip()
                        print(size)
                        cost = flat.find('div', class_='catalog-block-item-price').find('div',class_='catalog-block-item-price-total hidden').get_text().strip()
                        await db_pool.fetch(QUERY, size, cost)
                    except Exception as e:
                        print(e)
    except Exception as ex:
        print(ex)

async def main():
    tasks = []

    # асинк подкл к бд
    db_pool = await asyncpg.create_pool('postgresql://postgres:1234@localhost:5432/flat_db')

    for url in URLS:
        task = asyncio.create_task(parse_and_save(url, db_pool))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    init_db()
    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    end_time = time.time()
    print(f"Async time ': {end_time - start_time} seconds")