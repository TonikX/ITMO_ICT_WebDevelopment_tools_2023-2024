import threading
from typing import List
import requests
from bs4 import BeautifulSoup
import time
from database import add_article_to_database


def parse_and_save(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string
    add_article_to_database(processing_method="thread", url=url, title=title)


def main():
    urls = [
        "https://vk.com/",
        "https://habr.com/ru/all/",
        "https://student.itmo.ru/ru/expulsion_student_initiative/",
    ]

    threads: List[threading.Thread] = []

    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
