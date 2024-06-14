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
                page = await response.text()  # получаем страницу текстом
                soup = BeautifulSoup(page, 'html.parser')  # создаем парсер
                books = soup.find_all('div', class_='product-card')  # находим все блоки книг по классу
                for book in books:  # проходимся в цикле по всем книгам
                    title = book.attrs['data-product-name']  # получаем название книги
                    price = book.attrs['data-product-price-discounted']  # получаем цену книги

                    with db_conn.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                        cursor.execute(DBConn.INSERT_SQL, (title, price))  # выполняем ранее написанную команду и передаем в нее аргументы

                db_conn.commit()  # подтверждаем изменения
    except Exception as e:  # при получении исключения
        print("Ошибка:", e)  # выводим ошибку
        db_conn.rollback()  # откатываем изменения


async def process_url_list_async(url_list, conn):
    tasks = []  # создаем список корутин, где будут они храниться
    for url in url_list:  # проходимся циклом
        task = asyncio.create_task(parse_and_save_async(url, conn))  # и запускаем корутины
        tasks.append(task)  # добавляем к списку асинхронную функцию подсчета
    await asyncio.gather(*tasks)  # ожидаем выполнения всех заданий асинхронно


async def main():
    chunk_size = len(URLs) // number_of_threads  # определяем количество ссылок для каждой потока (2)
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]  # определяем сами ссылки

    db_conn = DBConn.connect_to_database()  # подключаемся к базе данных

    await asyncio.gather(
        *(process_url_list_async(chunk, db_conn) for chunk in url_chunks))  # ожидаем выполнения всех заданий асинхронно

    db_conn.close()  # закрываем подключение к базе данных


if __name__ == '__main__':
    start_time = time.time()  # засекаем начальное время
    asyncio.run(main())  # запускаем программу
    end_time = time.time()  # засекаем конечное время
    print(f"Время выполнения async: {end_time - start_time} секунд")  # выводим время выполнения
