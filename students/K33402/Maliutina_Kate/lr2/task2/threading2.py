import threading
import time
from connection import DBConn
import requests
from bs4 import BeautifulSoup
from data import URLs, number_of_threads


def parse_and_save_threading(url, db_conn):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
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


def process_url_list_threading(url_list, db_conn):
    for url in url_list:
        parse_and_save_threading(url, db_conn)


def main_threading():
    chunk_size = len(URLs) // number_of_threads
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]

    db_conn = DBConn.connect_to_database()

    threads = []
    for chunk in url_chunks:
        thread = threading.Thread(target=process_url_list_threading, args=(chunk, db_conn))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    db_conn.close()


if __name__ == '__main__':
    start_time = time.time()
    main_threading()
    end_time = time.time()
    print(f"Время выполнения threading: {end_time - start_time} секунд")
