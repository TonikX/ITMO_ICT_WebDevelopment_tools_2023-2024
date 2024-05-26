import multiprocessing
import time

import requests

from task_2.db import insert_user_data
from task_2.parse import extract_user_data

BASE_URL = 'https://moihottur.ru/companion/'
PAGINATION_KEY = 'page'
PAGES = 10


def fetch(url):
    return requests.get(url).text


def parse_and_save(url):
    page = fetch(url)
    user_data = extract_user_data(page)
    insert_user_data(user_data)


def main():
    tasks = [
        multiprocessing.Process(
            target=parse_and_save,
            args=(f'{BASE_URL}?{PAGINATION_KEY}={i}',),
        )
        for i in range(1, PAGES + 1)
    ]

    start_time = time.perf_counter()
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    end_time = time.perf_counter()

    print(f'Finished in {end_time - start_time:.3f} seconds')


if __name__ == '__main__':
    main()
