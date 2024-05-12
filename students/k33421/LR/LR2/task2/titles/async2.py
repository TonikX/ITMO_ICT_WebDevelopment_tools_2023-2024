import aiohttp
import asyncio
import asyncpg
from bs4 import BeautifulSoup
import time


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def parse_and_save(url):
    async with aiohttp.ClientSession() as session:

        html = await fetch(url, session)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text

        conn = await asyncpg.connect('postgresql://postgres:qwerty12345@localhost:5432/books')#psycopg2.connect("dbname=books user=postgres password=qwerty12345 host=localhost")
        try:

            await conn.execute("INSERT INTO titles (url, title) VALUES (%s, %s)", (url, title))
            print(url, title)
        finally:
            conn.close()


async def main(urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(parse_and_save(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":

    urls = [
        'https://pybitesbooks.com/',
        'https://books.toscrape.com'
    ]

    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(urls))
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Async time: {execution_time}")