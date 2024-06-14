import threading
import time
from connection import DBConn
import requests
from bs4 import BeautifulSoup
from data import URLs, number_of_threads


def parse_and_save_threading(url, db_conn):
    try:  # пробуем, поскольку может упасть исключение
        page = requests.get(url)  # получаем страницу
        soup = BeautifulSoup(page.text, 'html.parser')  # создаем парсер
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


def process_url_list_threading(url_list, db_conn):
    for url in url_list:  # в цикле берем каждую ссылку
        parse_and_save_threading(url, db_conn)  # и вызываем функцию парсинга


def main_threading():
    chunk_size = len(URLs) // number_of_threads  # определяем количество ссылок для каждого потока (2)
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]  # определяем сами ссылки

    db_conn = DBConn.connect_to_database()  # подключаемся к базе данных

    threads = []  # объявляем список потоков
    for chunk in url_chunks:  # проходимся циклом по ссылкам
        thread = threading.Thread(target=process_url_list_threading, args=(chunk, db_conn))  # создаем поток, передаем функцию обработчик и параметры
        threads.append(thread)  # включаем поток в список для отслеживания
        thread.start()  # запускаем поток

    for thread in threads:  # в цикле всех потоков
        thread.join()  # ожидаем его завершения

    db_conn.close()  # закрываем подключение к базе данных


if __name__ == '__main__':
    start_time = time.time()  # засекаем начальное время
    main_threading()  # запускаем программу
    end_time = time.time()  # засекаем конечное время
    print(f"Время выполнения threading: {end_time - start_time} секунд")  # выводим время выполнения
