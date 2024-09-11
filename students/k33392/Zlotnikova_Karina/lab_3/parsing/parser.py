import asyncio
import aiohttp
from bs4 import BeautifulSoup
import asyncpg

async def parse_and_save(url, db_url):
    db_pool = await asyncpg.create_pool(db_url)
    QUERY = """INSERT INTO vinil (author, name, cost) VALUES ($1, $2, $3)"""
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
                        await db_pool.fetch(QUERY, author, album_title, cost)
                    except Exception as e:
                        print(e)
    except Exception:
        print("Проблемы с чтением каталога")