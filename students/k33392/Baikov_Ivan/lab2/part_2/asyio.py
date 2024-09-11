import asyncio
import aiohttp
import time
import requests
from bs4 import BeautifulSoup
import asyncpg

from conn import sion, init_db
from models import *
from urls import URLS

QUERY = """INSERT INTO product (title, name, cost) VALUES ($1, $2, $3)"""


async def parse_and_save(url, db_pool):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                r = await response.text()
                soup = BeautifulSoup(r, 'html.parser')
                print("Type of furniture: ", soup.find('title').text)
                title = soup.find('title').text
                products = soup.find_all('div', class_="product-card__info")
                for product in products:
                    try:
                        name = product.find('div', class_='product-card__title').get_text().strip()
                        price = product.find('div', class_='product-card__buy-wrapper').find('div', class_='product-card__price-wrapper').get_text().strip()
                        price_info = price.split('\n')
                        price_info = price_info[0].strip()
                        await db_pool.fetch(QUERY,title, name, price_info)
                    except Exception as e:
                        print(e)
    except Exception as ex:
        print(ex)

async def main():
    tasks = []
    db_pool = await asyncpg.create_pool('postgresql://postgres:Scalapendra1219212712192127@localhost:5433/product_db')

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