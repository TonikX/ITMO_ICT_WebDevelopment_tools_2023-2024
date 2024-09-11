import asyncio
import aiohttp
import asyncpg
import time
from bs4 import BeautifulSoup
from db.db import init_db
from db.querys import QUERY_1
from db.url import urls, Db_url


async def parse_and_save(url, db_pool):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                r = await response.text()
                soup = BeautifulSoup(r, 'html.parser')
                vinils = soup.find_all('div', class_="album")
                for vinil in vinils:
                    try:
                        name = vinil.find('div', class_='album_cont').find('h4', class_='album_title').find('a')
                        start_author = str(name).find('>') + 1
                        end_author = str(name).find('<br')
                        author = str(name)[start_author:end_author].strip()
                        start_album = str(name).find('<br/>') + 5
                        end_album = str(name).find('</a')
                        album_title = str(name)[start_album:end_album].strip()
                        cost = vinil.find('div', class_='album_footer').find('div', class_='price').get_text().strip()
                        await db_pool.fetch(QUERY_1, author, album_title, cost)
                    except Exception:
                        print("Проблемы с чтением альбома")
    except Exception:
        print("Проблемы с чтением каталога")

async def main():
    tasks = []
    db_pool = await asyncpg.create_pool(Db_url)
    for url in urls:
        task = asyncio.create_task(parse_and_save(url, db_pool))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    init_db()
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Async': {end_time - start_time} s.")