import asyncio
import aiohttp
from bs4 import BeautifulSoup
import asyncpg
from product_models import *


async def parse_and_save(url, DATABASE_URL):
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    QUERY = """INSERT INTO product (title, name, cost) VALUES ($1, $2, $3)"""
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

