from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
from dotenv import load_dotenv
import os
import random

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
    num_process = len(urls) if len(urls) < 4 else 4
    pool = Pool(processes=num_process)
    pool.map(parse_and_save, urls)


if __name__ == "__main__":
    start_time = time.time()
    urls =  [
    f'https://mybooklist.ru/list/{random.randint(100, 1000)}' for _ in range(5)
    ]
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time

    with open('times.txt', 'a') as f:
        f.write(f"Multiprocess: {execution_time}\n")