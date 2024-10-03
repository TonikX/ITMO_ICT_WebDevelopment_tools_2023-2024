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

```python
import asyncio
import threading
import multiprocessing
import time

async def partial_sum_async(start, end):
    return sum(range(start, end))

def partial_sum_thread(start, end, results, index):
    total = sum(range(start, end))
    results[index] = total

def partial_sum_multiprocess(start, end):
    return sum(range(start, end))

async def calculate_sum_with_asyncio(n):
    num_tasks = 4
    step = n // num_tasks
    tasks = [partial_sum_async(i * step + 1, (i + 1) * step + 1 if i < num_tasks - 1 else n + 1) for i in range(num_tasks)]

    results = await asyncio.gather(*tasks)

    return sum(results)

def calculate_sum_with_threading(n):
    num_threads = 4
    threads = []
    results = [0] * num_threads
    step = n // num_threads

    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step + 1 if i < num_threads - 1 else n + 1
        thread = threading.Thread(target=partial_sum_thread, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)

def calculate_sum_with_multiprocessing(n):
    num_processes = 4
    pool = multiprocessing.Pool(processes=num_processes)
    step = n // num_processes
    tasks = [(i * step + 1, (i + 1) * step + 1 if i < num_processes - 1 else n + 1) for i in range(num_processes)]

    results = pool.starmap(partial_sum_multiprocess, tasks)
    pool.close()
    pool.join()

    return sum(results)

if __name__ == '__main__':
    n = 1000000
    start_time = time.time()
    result = calculate_sum_with_multiprocessing(n)
    end_time = time.time()

    print(f"Multiprocessing Result: {result}, Time: {end_time - start_time} seconds")

    start_time = time.time()
    result = asyncio.run(calculate_sum_with_asyncio(n))
    end_time = time.time()

    print(f"Asyncio Result: {result}, Time: {end_time - start_time} seconds")

    start_time = time.time()
    result = calculate_sum_with_threading(n)
    end_time = time.time()

    print(f"Threading Result: {result}, Time: {end_time - start_time} seconds")

```
## По итогу получилось:

| async | multiprocessing | threading |
|-------|-----------------|-----------|
| 0.854 | 0.689           | 0.705     |



# Задача 2

```python
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
        musicians = soup.find_all("figure", class_="component-chartlist-item with-counter")
        for musician in musicians:
            container = musician.find("figcaption")
            artist_name = container.find("a", class_="track-artist").text
            music_name = container.find("a", class_="track-title").text

            cursor.execute('INSERT INTO artists (artist, music) VALUES (?, ?)', (artist_name, music_name))

        conn.commit()


async def worker(urls, cursor, conn):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(url, session, cursor, conn) for url in urls]
        await asyncio.gather(*tasks)


async def main():
    urls = [
        "https://www.americantop40.com/charts/top-40-238/september-28-2024/",
        "https://www.americantop40.com/charts/top-40-238/august-17-2024/",
        "https://www.americantop40.com/charts/top-40-238/july-13-2024/"
    ]
    num_tasks = 3
    try:
        conn = sqlite3.connect('top.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist TEXT,
                music TEXT
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

## multiprocessing

```python
import multiprocessing

import requests
import sqlite3
from bs4 import BeautifulSoup
import time


def parse_and_save(url, queue):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    musicians = soup.find_all("figure", class_="component-chartlist-item with-counter")
    for musician in musicians:
        container = musician.find("figcaption")
        artist_name = container.find("a", class_="track-artist").text
        music_name = container.find("a", class_="track-title").text

        queue.put((artist_name, music_name))


def worker(urls, queue):
    for url in urls:
        parse_and_save(url, queue)


def main():
    urls = [
        "https://www.americantop40.com/charts/top-40-238/september-28-2024/",
        "https://www.americantop40.com/charts/top-40-238/august-17-2024/",
        "https://www.americantop40.com/charts/top-40-238/july-13-2024/"
    ]
    num_processes = 3
    queue = multiprocessing.Queue()
    processes = []
    conn = sqlite3.connect('top.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT,
            music TEXT
        )
    ''')

    start_time = time.time()

    for i in range(num_processes):
        process = multiprocessing.Process(target=worker, args=(urls[i::num_processes], queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        artist_name, music_name = queue.get()
        cursor.execute('INSERT INTO artists (artist, music) VALUES (?, ?)', (artist_name, music_name))

    conn.commit()
    conn.close()
    end_time = time.time()
    print(f"Parsed and saved data in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
```

## threading

```python
import threading
import requests
import sqlite3
from bs4 import BeautifulSoup
import time


def parse_and_save(url, cursor, conn):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    musicians = soup.find_all("figure", class_="component-chartlist-item with-counter")
    for musician in musicians:
        container = musician.find("figcaption")
        artist_name = container.find("a", class_="track-artist").text
        music_name = container.find("a", class_="track-title").text

        cursor.execute('INSERT INTO artists (artist, music) VALUES (?, ?)', (artist_name, music_name))

    conn.commit()


def worker(urls):
    conn = sqlite3.connect('top.db')
    cursor = conn.cursor()
    for url in urls:
        parse_and_save(url, cursor, conn)
    conn.close()


def main():
    urls = [
        "https://www.americantop40.com/charts/top-40-238/september-28-2024/",
        "https://www.americantop40.com/charts/top-40-238/august-17-2024/",
        "https://www.americantop40.com/charts/top-40-238/july-13-2024/"
    ]
    num_threads = 3

    conn = sqlite3.connect('top.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT,
            music TEXT
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

| async  | multiprocessing | threading |
|--------|-----------------|-----------|
| 0.0184 | 0.073           | 0.0285    |
# Выводы

Поработал, научился парсить сайт. Сравнил работу параллельной и асинхронной работы