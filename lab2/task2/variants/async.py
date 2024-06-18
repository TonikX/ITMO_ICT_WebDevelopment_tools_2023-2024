import aiohttp
import asyncio
import asyncpg
from bs4 import BeautifulSoup
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import *


async def save_to_db(data):
    conn = await asyncpg.connect("postgresql://postgres:1@localhost:5432/web_data")
    try:
        await conn.execute(
            "INSERT INTO site (url, title) VALUES ($1, $2)", data["url"], data["title"]
        )
    finally:
        await conn.close()


async def get_data(url, session):
    async with session.get(url) as response:
        return await response.text()


async def parse_and_save(url):
    async with aiohttp.ClientSession() as session:

        html = await get_data(url, session)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("title").text
        await save_to_db({"url": url, "title": title})


async def main(urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(parse_and_save(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":

    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(urls))
    end_time = time.time()
    execution_time = end_time - start_time
    file = open("times.txt", "a")

    file.write(f"Async time: {execution_time}\n")
