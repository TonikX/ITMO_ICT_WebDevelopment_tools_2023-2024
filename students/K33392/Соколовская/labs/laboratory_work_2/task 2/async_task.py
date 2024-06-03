import asyncio
from save_data_async import save_to_db
from parser_async import parse_data
import time

urls = [
    "https://www.litres.ru/author/kayl-simpson/",
    "https://www.litres.ru/author/robert-s-martin/",
    "https://www.litres.ru/author/darya-doncova/"
]


async def parse_and_save(url):
    author_info = await parse_data(url)
    await save_to_db(author_info)


async def start():
    start_time = time.time()

    tasks = []
    for url in urls:
        task = asyncio.create_task(parse_and_save(url))
        tasks.append(task)

    await asyncio.gather(*tasks)

    end_time = time.time()

    print("asynio")
    print(f"Время: {end_time - start_time} c")

if __name__ == '__main__':
    asyncio.run(start())
