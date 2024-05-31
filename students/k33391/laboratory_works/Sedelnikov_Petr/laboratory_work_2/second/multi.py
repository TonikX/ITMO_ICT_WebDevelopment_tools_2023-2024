import multiprocessing
import re

import requests
import sqlite3
from bs4 import BeautifulSoup
import time


def parse_litres(queue, category, params):
    r = requests.get(f"https://www.litres.ru/{category}", params=params)
    soup = BeautifulSoup(r.text, 'html.parser')
    books = soup.find_all('div', class_="ArtsGrid_artWrapper__LXa0O")
    count = 0
    for book in books:
        try:
            title = book.find('p', class_='ArtInfo_title__h_5Ay').get_text()
            author = book.find('a', class_='ArtInfo_author__0W3GJ').get_text()
            queue.put((title, author))
            count += 1
        except Exception as e:
            pass
    print(f"Litres: {count}")
    queue.put(None)


def parse_bookvoed(queue, category, params):
    r = requests.get(f"https://www.bookvoed.ru/{category}", params=params)
    soup = BeautifulSoup(r.text, 'html.parser')
    books = soup.find_all('div', class_="product-card")
    count = 0
    for book in books:
        try:
            title = book.find('a', class_='product-description__link').get_text()
            author = book.find('a', class_='ui-comma-separated-links__author').get_text()
            queue.put((title, author))
            count += 1
        except Exception as e:
            pass
    print(f"Bookvoed: {count}")
    queue.put(None)


def get_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    author TEXT
                )
            ''')
    conn.commit()
    return conn, cursor


def add_book(cursor, title, author):
    cursor.execute('INSERT INTO books (name, author) VALUES (?, ?)', (title, author))


def commit(conn):
    conn.commit()


def main():
    conn, cursor = get_db()
    queue = multiprocessing.Queue()
    processes = []

    first_process = multiprocessing.Process(target=parse_litres, args=(queue, 'genre/biznes-5003', {'art_types': 'text_book'}))
    processes.append(first_process)
    first_process.start()

    second_process = multiprocessing.Process(target=parse_bookvoed, args=(queue, 'catalog/business-1671', {}))
    processes.append(second_process)
    second_process.start()

    finished_processes = 0
    while finished_processes < 2:
        data = queue.get()
        if data is None:
            finished_processes += 1
        else:
            name, title = queue.get()
            add_book(cursor, name, title)

    commit(conn)


if __name__ == "__main__":
    print("Multiprocessing")
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
