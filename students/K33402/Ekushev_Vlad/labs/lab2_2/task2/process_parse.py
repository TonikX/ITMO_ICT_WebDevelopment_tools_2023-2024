import multiprocessing
from typing import List
import requests
from bs4 import BeautifulSoup
import time
from database import add_article_to_database


def parse_and_save(url: str):
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text, "html.parser")
    title = parsed_html.title.string
    add_article_to_database(processing_method="process", url=url, title=title)


def main():
    urls = [
        "https://vk.com/",
        "https://habr.com/ru/all/",
        "https://student.itmo.ru/ru/expulsion_student_initiative/",
    ]

    processes: List[multiprocessing.Process] = []

    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
