from threading import Thread
import requests
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import random
import psycopg2
import os

load_dotenv()

def save_to_database(url, title):
    db_url = os.getenv("DB_URL")
    conn = psycopg2.connect(db_url)
    curs = conn.cursor()

    curs.execute("INSERT INTO site (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()


def parse_and_save(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    save_to_database(url, title)


def main(urls):

    threads = []
    for url in urls:
        thread = Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start_time = time.time()
    urls =  [
    f'https://mybooklist.ru/list/{random.randint(100, 1000)}' for _ in range(5)
    ]
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time

    with open('times.txt', 'a') as f:
        f.write(f"Tread: {execution_time}\n")