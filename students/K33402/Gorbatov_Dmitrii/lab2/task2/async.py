import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
from database import get_session, Site, init_db

init_db()

async def parse_and_save_async(url: str) -> None:
    async with aiohttp.ClientSession() as session:
            response = await fetch_page(session, url)
            soup = BeautifulSoup(response, 'html.parser')
            title = soup.title.string
            session = get_session()
            site = Site(url=url, title=title, method='async')
            session.add(site)
            session.commit()
            session.refresh(site)

            print(f"{url} - {title}")


async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, ssl=False) as response:
        return await response.text()

async def asyncio_example():
    urls = [
        'https://www.example.com',
        'https://www.google.com',
        'https://www.python.org',
        'https://www.stackoverflow.com',
        'https://www.github.com'
    ]

    tasks = [parse_and_save_async(url) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(asyncio_example())
    end_time = time.time()
    print(f"Asyncio time: {end_time - start_time:.4f} seconds")