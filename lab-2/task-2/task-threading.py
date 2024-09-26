import threading
import requests
import sqlite3
from bs4 import BeautifulSoup
import re
import time


def parse_and_save(url, cursor, conn):
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

            cursor.execute('INSERT INTO finance (url, name, balance) VALUES (?, ?, ?)', (url, name, balance))
    conn.commit()


def worker(urls):
    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()
    for url in urls:
        parse_and_save(url, cursor, conn)
    conn.close()


def main():
    urls = ["https://www.forbes.ru/milliardery/487053-10-bogatejsih-ludej-mira-2023-rejting-forbes"]
    num_threads = 3

    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()

    # Создаем таблицу, если она еще не создана
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            name TEXT,
            balance TEXT
        )
    ''')
    conn.commit()
    conn.close()

    threads = []
    start_time = time.time()

    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(urls[i::num_threads],))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Parsed and saved data in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
