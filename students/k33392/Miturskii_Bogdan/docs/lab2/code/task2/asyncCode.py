import asyncio
import aiohttp
from bs4 import BeautifulSoup
from sqlmodel import Session
from database import WebPage, create_db_and_tables, engine
import sys

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_and_save(url, session):
    try:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'

        with Session(engine) as db_session:
            webpage = WebPage(url=url, title=title)
            db_session.add(webpage)
            db_session.commit()
    except Exception as e:
        print(f"Ошибка парсинга {url}: {e}")

async def main(urls):
    create_db_and_tables()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(parse_and_save(url, session))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import time
    urls = sys.argv[1:]
    if not urls:
        print("Не предоставлены url для парсинга")
        sys.exit(1)
    start_time = time.time()
    asyncio.run(main(urls))
    end_time = time.time()
    print(f"Async/await занял: {end_time - start_time} секунд")
