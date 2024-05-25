import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup
from connection import DBConn
from data import URLs, number_of_threads


async def parse_and_save_async(url, db_conn):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                page = await response.text()
                soup = BeautifulSoup(page, 'html.parser')
                books = soup.find_all('div', class_='product-card')
                for book in books:
                    title = book.attrs['data-product-name']
                    price = book.attrs['data-product-price-discounted']

                    with db_conn.cursor() as cursor:
                        cursor.execute(DBConn.INSERT_SQL, (title, price))

                db_conn.commit()
    except Exception as e:
        print("Ошибка:", e)
        db_conn.rollback()


async def process_url_list_async(url_list, conn):
    tasks = []
    for url in url_list:
        task = asyncio.create_task(parse_and_save_async(url, conn))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def main():
    chunk_size = len(URLs) // number_of_threads
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]
    db_conn = DBConn.connect_to_database()

    await asyncio.gather(*(process_url_list_async(chunk, db_conn) for chunk in url_chunks))

    db_conn.close()


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Время выполнения async: {end_time - start_time} секунд")
