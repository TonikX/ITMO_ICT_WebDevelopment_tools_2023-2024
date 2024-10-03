import ssl

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/top')


async def parse_and_save(url, session, database):
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

            query = 'INSERT INTO artists (artist, music) VALUES (:artist_name, :music_name)'
            values = {"artist_name": artist_name, "music_name": music_name}

            await database.execute(query, values)


async def worker(urls, database):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(url, session, database) for url in urls]
        await asyncio.gather(*tasks)


async def main_start():
    urls = ["https://www.americantop40.com/charts/top-40-238/september-28-2024/"]
    num_tasks = 1
    database = Database(DATABASE_URL)
    try:
        await database.connect()
        await database.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                id SERIAL PRIMARY KEY,
                artist TEXT,
                music TEXT
            )
        ''')

        start_time = time.time()

        tasks = [asyncio.create_task(worker(urls[i::num_tasks], database)) for i in range(num_tasks)]

        await asyncio.gather(*tasks)

        await database.disconnect()
        end_time = time.time()
        print(f"Parsed and saved data in {end_time - start_time} seconds")
    except Exception as e:
        print(f"Unexpected error: {e}")