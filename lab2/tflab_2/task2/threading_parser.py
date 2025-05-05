import threading
import time

import requests

from tflab_2.task2.common.parser import process_page
from tflab_2.task2.urls import urls


def parse_and_save(url_list):
    for url in url_list:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        process_page(response.text)


def main():
    num_threads = 5
    start_time = time.time()
    chunk_size = (len(urls) + num_threads - 1) // num_threads
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=parse_and_save, args=(chunk,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Количество потоков: {num_threads}")
    print(f"Время выполнения при помощи threading: {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    main()
