import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
from database import add_article_to_database


async def parse_and_save(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        html = await response.text()
        parsed_html = BeautifulSoup(html, "html.parser")
        title = parsed_html.title.string
        add_article_to_database(processing_method="async", url=url, title=title)


async def main():
    urls = [
        "https://vk.com/",
        "https://habr.com/ru/all/",
        "https://student.itmo.ru/ru/expulsion_student_initiative/",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
