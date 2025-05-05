import multiprocessing
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
    start_time = time.time()
    num_processes = 5
    chunk_size = (len(urls) + num_processes - 1) // num_processes
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    processes = []

    for chunk in chunks:
        process = multiprocessing.Process(target=parse_and_save, args=(chunk,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Количество процессов: {num_processes}")
    print(f"Время выполнения при помощи multiprocessing: {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    main()
