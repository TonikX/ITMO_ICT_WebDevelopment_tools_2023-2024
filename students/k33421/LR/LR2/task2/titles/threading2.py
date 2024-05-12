from threading import Thread
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

    threads = []
    for url in urls:
        thread = Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":

    urls = [
        'https://pybitesbooks.com/',
        'https://books.toscrape.com'
        ]

    pages = [1, 2, 3]

    start_time = time.time()
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Threading time: {execution_time}")