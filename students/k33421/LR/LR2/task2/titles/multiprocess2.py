from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import psycopg2
import time


def parse_and_save(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text

    conn = psycopg2.connect("dbname=books user=postgres password=qwerty12345 host=localhost")
    curs = conn.cursor()

    curs.execute("INSERT INTO titles (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()

    print(url, title)


def main(urls):

    num_process = len(urls) if len(urls) < 4 else 4
    pool = Pool(processes=num_process)
    pool.map(parse_and_save, urls)


if __name__ == "__main__":

    urls = [
        'https://pybitesbooks.com/',
        'https://books.toscrape.com'
    ]

    start_time = time.time()
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Multiprocessing time: {execution_time}")
