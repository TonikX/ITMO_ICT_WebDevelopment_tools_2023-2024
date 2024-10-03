import asyncio
import aiohttp
from time import time
from bs4 import BeautifulSoup
from parsing import URLS2, pars_item_ebay, insert_into_db

async def fetch(session, url):
    async with session.get(url) as response:
        print("Status code: " + str(response.status))
        return await response.text()

async def parse_and_save(session, url):
    print("Отправляем запрос")
    try:
        text = await fetch(session, url)

        soup = BeautifulSoup(text, 'html.parser')
        items = soup.find_all('li', class_='s-item')

        parsed_items = []
        for item in items:
            item_res = pars_item_ebay(item)
            parsed_items.append(item_res)

        insert_into_db(parsed_items)

    except aiohttp.ClientError as e:
        print(f"Error req: {url}\n{e}")

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = parse_and_save(session, url)
            tasks.append(task)
        await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    start = time()
    asyncio.run(main(URLS2))
    end = time()
    print("Time: " + str(end - start))