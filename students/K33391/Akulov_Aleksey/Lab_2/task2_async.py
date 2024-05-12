import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def parse_and_save(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text if soup.find('title') else 'No title found'
        print(f'Processed {url}: {title}')
        # Сохранение в базу данных, аналогично threading

async def main_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)

urls = ['https://example.com', 'https://example.org', 'https://example.net']
asyncio.run(main_async(urls))
