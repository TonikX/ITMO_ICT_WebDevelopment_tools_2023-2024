import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time

async def parse_and_save(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text if soup.find('title') else 'No title found'
        print(f'Processed {url}: {title}')
        # сохранение в базу данных

async def main_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = time.perf_counter()
    urls = ["https://habr.com/ru/flows/develop/articles/"]
    asyncio.run(main_async(urls))
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time} секунд")