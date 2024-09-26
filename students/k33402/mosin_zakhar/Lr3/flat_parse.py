import asyncio
import aiohttp
from bs4 import BeautifulSoup
import asyncpg
from flat_mod import *

async def parse_and_save(url, DATABASE_URL):
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    QUERY = """INSERT INTO flat (size, cost) VALUES ($1, $2)"""
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

