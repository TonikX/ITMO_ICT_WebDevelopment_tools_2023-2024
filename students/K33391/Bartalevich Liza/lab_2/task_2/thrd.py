from threading import Thread
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
from urls import urls


def parse_and_save(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text  

    conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/web_data')
    curs = conn.cursor()

    curs.execute("INSERT INTO site (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()


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
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Threading time: {execution_time}")