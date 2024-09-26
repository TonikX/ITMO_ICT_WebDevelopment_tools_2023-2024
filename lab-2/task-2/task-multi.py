import multiprocessing
import re

import requests
import sqlite3
from bs4 import BeautifulSoup
import time


def parse_and_save(url, queue):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    billionaires = soup.find_all("figcaption", class_="EXdHT")
    for billionaire in billionaires:
        name_tag = billionaire.find("h2", class_="jYzxi")
        balance_tag = billionaire.find("p", class_="ywx5e Q0w8z")

        if name_tag and balance_tag:
            name = name_tag.text.strip().split(" ", 1)[-1]  # Извлекаем имя без "№2"
            balance_text = balance_tag.find("b", string=re.compile(r"Состояние:\s*"))
            if balance_text:
                balance = balance_text.next_sibling.strip()
            else:
                balance = "Неизвестно"

            queue.put((url, name, balance))


def worker(urls, queue):
    for url in urls:
        parse_and_save(url, queue)


def main():
    urls = ["https://www.forbes.ru/milliardery/487053-10-bogatejsih-ludej-mira-2023-rejting-forbes"]
    num_processes = 3
    queue = multiprocessing.Queue()
    processes = []
    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()

    start_time = time.time()

    for i in range(num_processes):
        process = multiprocessing.Process(target=worker, args=(urls[i::num_processes], queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        url, name, balance = queue.get()
        cursor.execute('INSERT INTO finance (url, name, balance) VALUES (?, ?, ?)', (url, name, balance))

    conn.commit()
    conn.close()
    end_time = time.time()
    print(f"Parsed and saved data in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
