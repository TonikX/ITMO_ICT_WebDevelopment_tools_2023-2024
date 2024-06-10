import asyncio
import aiohttp
import time
import config

from connection import DataBaseConnection
from bs4 import BeautifulSoup
from datetime import date, timedelta


async def parse_and_save(url, db_conn):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                tasks = soup.find_all(config.HTML_TAG, class_=config.HTML_CLASS)
                tasks = [task.text.strip().replace('\xa0', ' ') for task in tasks]

                with db_conn.cursor() as cursor:
                    for task in tasks:
                        cursor.execute(DataBaseConnection.INSERT_SQL,
                                       (task, '', str(date.today()), str(date.today() + timedelta(7)),
                                        'high', 'to_do', 2, 3))

                db_conn.commit()
    except Exception as e:
        print("Error:", e)


async def process_url_list(url_list, conn):
    tasks = []
    for url in url_list:
        task = asyncio.create_task(parse_and_save(url, conn))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def main():
    urls = config.URLS
    num_threads = config.NUM_THREADS
    chunk_size = len(urls) // num_threads
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    db_conn = DataBaseConnection.connect_to_database()
    start_time = time.time()

    await asyncio.gather(*(process_url_list(chunk, db_conn) for chunk in url_chunks))

    db_conn.close()
    end_time = time.time()

    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == '__main__':
    asyncio.run(main())
