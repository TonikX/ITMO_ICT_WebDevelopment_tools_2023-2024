import threading
import requests
from bs4 import BeautifulSoup
import psycopg2
import time


def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text

    conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/labs')
    curs = conn.cursor()

    curs.execute("INSERT INTO site (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()


def main_threading(urls):
    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start_time = time.perf_counter()
    urls = ["https://habr.com/ru/companies/ussc/articles/833348/"]
    main_threading(urls)
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time} секунд")