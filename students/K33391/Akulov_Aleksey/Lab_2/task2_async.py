import asyncio

import time

import aiohttp
from bs4 import BeautifulSoup

from common import URLS, pars_item, PAGES, insert_into_db


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_and_save(session, url):
    for page in PAGES:
        complete_url = f'{url}{page}'
        try:
            text = await fetch(session, complete_url)
        except aiohttp.ClientError as e:
            print(f"Ошибка запроса на страницу: {complete_url}\n{e}")
            continue

        soup = BeautifulSoup(text, 'html.parser')
        items = soup.find_all('li', class_='s-item')

        parsed_items = []
        for item in items:
            item_res = pars_item(item)
            parsed_items.append(item_res)

        insert_into_db(parsed_items)
async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = parse_and_save(session, url)
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(URLS))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Async time: {execution_time}")
