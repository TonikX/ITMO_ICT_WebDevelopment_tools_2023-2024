import ssl

import aiohttp
import asyncio
import sqlite3
from bs4 import BeautifulSoup
import time


async def parse_and_save(url, session, cursor, conn):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with session.get(url, ssl=ssl_context) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        musicians = soup.find_all("figure", class_="component-chartlist-item with-counter")
        for musician in musicians:
            container = musician.find("figcaption")
            artist_name = container.find("a", class_="track-artist").text
            music_name = container.find("a", class_="track-title").text

            cursor.execute('INSERT INTO artists (artist, music) VALUES (?, ?)', (artist_name, music_name))

        conn.commit()


async def worker(urls, cursor, conn):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(url, session, cursor, conn) for url in urls]
        await asyncio.gather(*tasks)


async def main():
    urls = [
        "https://www.americantop40.com/charts/top-40-238/september-28-2024/",
        "https://www.americantop40.com/charts/top-40-238/august-17-2024/",
        "https://www.americantop40.com/charts/top-40-238/july-13-2024/"
    ]
    num_tasks = 3
    try:
        conn = sqlite3.connect('top.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist TEXT,
                music TEXT
            )
        ''')
        conn.commit()

        start_time = time.time()

        tasks = []
        for i in range(num_tasks):
            task = asyncio.create_task(worker(urls[i::num_tasks], cursor, conn))
            tasks.append(task)

        await asyncio.gather(*tasks)

        conn.close()
        end_time = time.time()
        print(f"Parsed and saved data in {end_time - start_time} seconds")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())