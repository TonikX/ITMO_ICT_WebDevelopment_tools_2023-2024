import multiprocessing
import time
import config
import requests

from bs4 import BeautifulSoup
from datetime import date, timedelta
from connection import DataBaseConnection


def parse_and_save(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            tasks = soup.find_all(config.HTML_TAG, class_=config.HTML_CLASS)
            tasks = [task.text.strip().replace('\xa0', ' ') for task in tasks]
        else:
            tasks = []

        with DataBaseConnection.connect_to_database() as db_conn:
            with db_conn.cursor() as cursor:
                for task in tasks:
                    cursor.execute(DataBaseConnection.INSERT_SQL,
                                   (task, '', str(date.today()), str(date.today() + timedelta(7)),
                                    'high', 'to_do', 2, 3))

        db_conn.commit()
    except Exception as e:
        print("Error:", e)


def process_url_list(url_queue):
    for url in url_queue:
        parse_and_save(url)


def main():
    urls = config.URLS
    num_threads = config.NUM_THREADS
    chunk_size = len(urls) // num_threads
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    start_time = time.time()
    processes = []

    for chunk in url_chunks:
        process = multiprocessing.Process(target=process_url_list, args=(chunk,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    end_time = time.time()

    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
