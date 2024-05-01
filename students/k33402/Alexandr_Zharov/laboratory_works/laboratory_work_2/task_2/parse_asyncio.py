import asyncio
import aiohttp
from bs4 import BeautifulSoup
import sqlite3
import time


def create_table_if_not_exists():
    conn = sqlite3.connect('data_3.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pages (
                    id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL)''')
    conn.commit()
    conn.close()


async def parse_and_save(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string

        conn = sqlite3.connect('data_3.db')
        cur = conn.cursor()

        cur.execute("INSERT INTO pages (url, title) VALUES (?, ?)", (url, title))
        conn.commit()

        print(f"Title of {url}: {title}")

        cur.close()
        conn.close()


async def main():
    urls = ["https://github.com/", "https://gitlab.com/", "https://hd.kinopoisk.ru/"]

    create_table_if_not_exists()

    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

