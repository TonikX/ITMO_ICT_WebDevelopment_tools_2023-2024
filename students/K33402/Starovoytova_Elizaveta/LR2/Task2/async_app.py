import asyncio
import aiohttp
import json
from save_data_async import save_author_and_books_from_json
from async_parser import parse_author_info
import time

# Список URL-адресов для парсинга
urls = ["https://www.litres.ru/author/patrik-king/",
        "https://www.litres.ru/author/vladimir-pozner/",
        "https://www.litres.ru/author/allan-dib/"]


async def parse_and_save(url):
    author_info = await parse_author_info(url)
    await save_author_and_books_from_json(author_info)


async def main():
    start_time = time.time()

    tasks = []
    for url in urls:
        task = asyncio.create_task(parse_and_save(url))
        tasks.append(task)

    await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time} секунд")


if __name__ == "__main__":
    asyncio.run(main())
