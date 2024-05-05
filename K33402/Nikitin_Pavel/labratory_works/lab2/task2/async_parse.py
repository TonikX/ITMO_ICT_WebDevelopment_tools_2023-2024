import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
from database import commit_article

async def parse_and_save(session, url):
    async with session.get(url) as response:
        html = await response.text()
        parsed_html = BeautifulSoup(html, 'html.parser')
        title = parsed_html.title.string
        commit_article(title)


async def main():
    urls = ["https://zoom.us/", "https://www.skype.com/", "https://discord.com/"]

    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")