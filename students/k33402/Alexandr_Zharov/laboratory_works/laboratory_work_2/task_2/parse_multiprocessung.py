import multiprocessing
import requests
from bs4 import BeautifulSoup
import sqlite3
import time


def create_table_if_not_exists():
    conn = sqlite3.connect('data_2.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pages (
                    id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string

    conn = sqlite3.connect('data_2.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO pages (url, title) VALUES (?, ?)", (url, title))
    conn.commit()

    print(f"Title of {url}: {title}")

    cur.close()
    conn.close()


def main():
    urls = ["https://github.com/", "https://gitlab.com/", "https://hd.kinopoisk.ru/"]

    create_table_if_not_exists()

    processes = []

    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
