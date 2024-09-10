import threading
import time
from connection import DBConn
import requests
from bs4 import BeautifulSoup
from data import URLs, number_of_threads


def parse_and_save_threading(url, db_conn):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')  # создаем парсер
        articles = soup.find_all('article', class_='tm-articles-list__item')
        for article in articles:
            author = article.find('a', class_='tm-user-info__username').text
            datetime = article.find('a', class_='tm-article-datetime-published tm-article-datetime-published_link').text
            title = article.find('a', class_='tm-title__link').text

            with db_conn.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                cursor.execute(DBConn.INSERT_SQL, (title, author, datetime))

        db_conn.commit()
    except Exception as e:
        print("Ошибка:", e)
        db_conn.rollback()


def process_url_list_threading(url_list, db_conn):
    for url in url_list:  # в цикле берем каждую ссылку
        parse_and_save_threading(url, db_conn)  # и вызываем функцию парсинга


def main_threading():
    chunk_size = len(URLs) // number_of_threads  # определяем количество ссылок для каждого потока (2)
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]  # определяем сами ссылки

    db_conn = DBConn.connect_to_database()

    threads = []
    for chunk in url_chunks:
        thread = threading.Thread(target=process_url_list_threading, args=(chunk, db_conn))
        threads.append(thread)
        thread.start()

    for thread in threads:  # в цикле всех потоков
        thread.join()  # ожидаем его завершения

    db_conn.close()


if __name__ == '__main__':
    start_time = time.time()
    main_threading()
    end_time = time.time()
    print(f"Время выполнения threading: {end_time - start_time} секунд")
