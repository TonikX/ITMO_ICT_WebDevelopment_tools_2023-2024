import multiprocessing
import time
import requests
from bs4 import BeautifulSoup
from connection import DBConn
from data import URLs, number_of_threads


def parse_and_save_multiprocessing(url):
    db_conn = DBConn.connect_to_database()  # подключаемся к базе данных
    try:
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
    finally:  # в конце всегда закрываем соединение с базой данных
        db_conn.close()


def process_url_list_multiprocessing(url_list):
    for url in url_list:  # в цикле берем каждую ссылку
        parse_and_save_multiprocessing(url)  # и вызываем функцию парсинга


def main_multiprocessing():
    chunk_size = len(URLs) // number_of_threads  # определяем количество ссылок для каждого процесса (2)
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]  # определяем сами ссылки

    processes = []  # объявляем список процессов
    for chunk in url_chunks:  # проходимся циклом по ссылкам
        process = multiprocessing.Process(target=process_url_list_multiprocessing, args=(chunk,))  # создаем поток, передаем функцию обработчик и параметры через tuple
        processes.append(process)  # включаем процесс в список для отслеживания
        process.start()  # запускаем процесс

    for process in processes:  # в цикле всех процессов
        process.join()  # ожидаем его завершения


if __name__ == '__main__':
    start_time = time.time()  # засекаем начальное время
    main_multiprocessing()  # запускаем программу
    end_time = time.time()  # засекаем конечное время
    print(f"Время выполнения multiprocessing: {end_time - start_time} секунд")  # выводим время выполнения
