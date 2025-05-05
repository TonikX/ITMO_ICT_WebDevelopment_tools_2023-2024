import asyncio
import time

import aiohttp

from tflab_2.task2.common.parser import process_page
from tflab_2.task2.urls import urls


async def fetch(session, url):
    async with session.get(url, timeout=10, ssl=False) as response:
        text = await response.text()
        return url, text


async def parse_and_save(url):
    async with aiohttp.ClientSession() as session:
        url, html = await fetch(session, url)
        if html:
            process_page(html)

async def parse_chunk(chunk):
    tasks = [parse_and_save(url) for url in chunk]
    await asyncio.gather(*tasks)


async def main():
    num_chunks = 5
    start_time = time.time()

    chunk_size = (len(urls) + num_chunks - 1) // num_chunks
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    chunk_tasks = [parse_chunk(chunk) for chunk in chunks]
    await asyncio.gather(*chunk_tasks)

    print(f"Количество задач: {len(urls)}")
    print(f"Время выполнения при помощи asyncio + aiohttp: {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    asyncio.run(main())
