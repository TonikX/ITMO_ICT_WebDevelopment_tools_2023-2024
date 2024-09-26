from multiprocessing import Process
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

def main_multiprocessing(urls):
    processes = []
    for url in urls:
        process = Process(target=parse_and_save, args=(url))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


if __name__ == "__main__":
    start_time = time.perf_counter()
    urls = ["https://habr.com/ru/flows/develop/articles/"]
    main_multiprocessing(urls)
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time} секунд")