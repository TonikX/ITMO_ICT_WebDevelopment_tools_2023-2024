import asyncio
import aiohttp
from bs4 import BeautifulSoup
from sqlmodel import Session
from database.models import WebPage
from database.database import create_db_and_tables, engine

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
            return {"url": url, "title": title}
    except Exception as e:
        print(f"Ошибка парсинга {url}: {e}")
        return {"url": url, "title": None, "error": str(e)}

async def main(urls):
    create_db_and_tables()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(parse_and_save(url, session))
        results = await asyncio.gather(*tasks)
        return results
