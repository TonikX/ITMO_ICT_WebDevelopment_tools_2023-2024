# Лабораторная работа №2

Задание:
Задача 1. Различия между threading, multiprocessing и async в Python
Задача: Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async.
Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных
задач для ускорения выполнения.

Подробности задания:

Напишите программу на Python для каждого подхода: threading, multiprocessing и async.
Каждая программа должна содержать функцию calculate_sum(), которая будет выполнять вычисления.
Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова
async/await и модуль asyncio.
Каждая программа должна разбить задачу на несколько подзадач и выполнять их параллельно.
Замерьте время выполнения каждой программы и сравните результаты.
Задача 2. Параллельный парсинг веб-страниц с сохранением в базу данных
Задача: Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу
данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с
нескольких веб-сайтов, сохранять их в базу данных.

Подробности задания:

Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async.
Каждая программа должна содержать функцию parse_and_save(url), которая будет загружать HTML-страницу по указанному URL,
парсить ее, сохранять заголовок страницы в базу данных и выводить результат на экран.
Используйте базу данных из лабораторной работы номер 1 для заполенния ее данными. Если Вы не понимаете, какие таблицы и
откуда Вы могли бы заполнить с помощью парсинга, напишите преподавателю в общем чате потока.
Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова
async/await и модуль aiohttp для асинхронных запросов.
Создайте список нескольких URL-адресов веб-страниц для парсинга и разделите его на равные части для параллельного
парсинга.
Запустите параллельный парсинг для каждой программы и сохраните данные в базу данных.
Замерьте время выполнения каждой программы и сравните результаты.
Дополнительные требования:

Сделайте документацию, содержащую описание каждой программы, используемые подходы и их особенности.
Включите в документацию таблицы, отображающие время выполнения каждой программы.
Прокомментируйте результаты сравнения времени выполнения программ на основе разных подходов

# Ход работы

## async

```python
import asyncio
import time


async def calculate_sum(start, end):
    return sum(range(start, end))


async def worker(start, end, results, index):
    results[index] = await calculate_sum(start, end)


async def main():
    num_tasks = 4
    n = 1000000
    step = n // num_tasks
    tasks = []
    results = [0] * num_tasks

    start_time = time.time()
    for i in range(num_tasks):
        start = i * step + 1
        end = (i + 1) * step + 1
        task = asyncio.create_task(worker(start, end, results, i))
        tasks.append(task)

    await asyncio.gather(*tasks)

    total_sum = sum(results)
    end_time = time.time()
    print(f"Total sum is {total_sum}, computed in {end_time - start_time} seconds")


if __name__ == "__main__":
    asyncio.run(main())

```

## multiprocessing

```python
import multiprocessing
import time


def calculate_sum(start, end):
    return sum(range(start, end))


def worker(start, end, queue):
    queue.put(calculate_sum(start, end))


def main():
    num_processes = 4
    n = 1000000
    step = n // num_processes
    processes = []
    queue = multiprocessing.Queue()

    start_time = time.time()
    for i in range(num_processes):
        start = i * step + 1
        end = (i + 1) * step + 1
        process = multiprocessing.Process(target=worker, args=(start, end, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = sum(queue.get() for _ in range(num_processes))
    end_time = time.time()
    print(f"Total sum is {total_sum}, computed in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
```

## threading

```python
import threading
import time


def calculate_sum(start, end):
    return sum(range(start, end))


def worker(start, end, result, index):
    result[index] = calculate_sum(start, end)


def main():
    num_threads = 4
    n = 1000000
    step = n // num_threads
    threads = []
    results = [0] * num_threads

    start_time = time.time()
    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step + 1
        thread = threading.Thread(target=worker, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    end_time = time.time()
    print(f"Total sum is {total_sum}, computed in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()

```

## По итогу получилось:

| async  | multiprocessing | threading |
|--------|-----------------|-----------|
| 0.0084 | 0.083           | 0.0085    |

# Задача 2
```python
import sqlite3


def create_database():
    conn = sqlite3.connect('personal_finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            balance TEXT
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()

```
```python
import re
import ssl

import aiohttp
import asyncio
import sqlite3
from bs4 import BeautifulSoup
import time


async def parse_and_save(url, session, cursor, conn):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with session.get(url, ssl=ssl_context) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')

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


async def worker(urls, cursor, conn):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(url, session, cursor, conn) for url in urls]
        await asyncio.gather(*tasks)


async def main():
    urls = ["https://www.forbes.ru/milliardery/487053-10-bogatejsih-ludej-mira-2023-rejting-forbes"]
    num_tasks = 1
    try:
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

        start_time = time.time()

        tasks = []
        for i in range(num_tasks):
            task = asyncio.create_task(worker(urls[i::num_tasks], cursor, conn))
            tasks.append(task)

        await asyncio.gather(*tasks)

        conn.close()
        end_time = time.time()
        print(f"Parsed and saved data in {end_time - start_time} seconds")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

```
```python
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

```

```python
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

```
## По итогу получилось:

| async | multiprocessing | threading |
|-------|-----------------|-----------|
| 0.851 | 1.029           | 0.805     |


# Выводы

Поработал, научился парсить сайт. Сравнил работу параллельной и асинхронной работы