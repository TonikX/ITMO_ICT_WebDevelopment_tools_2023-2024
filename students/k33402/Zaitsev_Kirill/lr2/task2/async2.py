import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup
from connection import DBConn
from data import URLs, number_of_threads


async def parse_and_save_async(url, db_conn):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:  # асинхронно создаем клиент-сессию для совершения запросов
            async with session.get(url) as response:  # асинхронно получаем ответ по ссылке из клиента-сессии
                page = await response.text()
                soup = BeautifulSoup(page, 'html.parser')  # создаем парсер
                articles = soup.find_all('article', class_='tm-articles-list__item')
                for article in articles:
                    author = article.find('a', class_='tm-user-info__username').text
                    datetime = article.find('a',
                                            class_='tm-article-datetime-published tm-article-datetime-published_link').text
                    title = article.find('a', class_='tm-title__link').text

                    with db_conn.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                        cursor.execute(DBConn.INSERT_SQL, (title, author, datetime))

                db_conn.commit()
    except Exception as e:
        print("Ошибка:", e)
        db_conn.rollback()


async def process_url_list_async(url_list, conn):
    tasks = []  # создаем список корутин, где будут они храниться
    for url in url_list:
        task = asyncio.create_task(parse_and_save_async(url, conn))
        tasks.append(task)
    await asyncio.gather(*tasks)  # ожидаем выполнения всех заданий асинхронно


async def main():
    chunk_size = len(URLs) // number_of_threads  # определяем количество ссылок для каждой потока (2)
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]  # определяем сами ссылки

    db_conn = DBConn.connect_to_database()

    await asyncio.gather(*(process_url_list_async(chunk, db_conn) for chunk in url_chunks))
    # ожидаем выполнения всех заданий асинхронно

    db_conn.close()


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Время выполнения async: {end_time - start_time} секунд")
