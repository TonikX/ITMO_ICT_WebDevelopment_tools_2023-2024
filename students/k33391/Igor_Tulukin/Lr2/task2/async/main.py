import aiohttp
import asyncio
from bs4 import BeautifulSoup
import psycopg2
import time

DB_URL = 'postgresql://postgres:12345@localhost/finances'


async def save_to_db(url, title):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO page (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()
    cursor.close()
    conn.close()


async def parse_and_save(session, url):
    async with session.get(url) as response:
        content = await response.text()
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
        await save_to_db(url, title)
        print(f"Processed: {url} with title: {title}")


async def main():
    urls = [
        'https://www.yahoo.com',
        'https://www.stackoverflow.com',
        'https://www.duckduckgo.com',
    ]

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Async finished in {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
