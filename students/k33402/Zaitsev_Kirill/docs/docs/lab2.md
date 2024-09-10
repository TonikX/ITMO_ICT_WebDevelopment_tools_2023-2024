# Lab 2

Подытог: создание процесса дороже создания потока, создание потока дороже создания рутины.
Время выполнения в среднем у async < threading < multiprocessing.

## Code + screenshots
### async1.py
Создаем нужное количество (ко/го)рутин и делим 1_000_000 на их количество. Каждая единица выполнит функцию, которая суммирует все точки данного отрезка и результат добавит в лист.
После выполнения суммируются результаты и выводится в консоли вместе с временем выполнения.
```python
import asyncio
from time import time


# функция подсчета суммы в заданном диапозоне
async def calculate_sum(start, end):
    s = sum(range(start, end + 1))
    return s


async def main():
    start_time = time()
    task_count = 5  # выполняться программа будет в 5 корутин
    numbers_per_task = 1_000_000 // task_count  # в каждой корутине будет считаться сумма 200_000 чисел
    tasks = list()

    for i in range(task_count):  # проходимся циклом и запускаем корутины
        start = i * numbers_per_task + 1  # первый индекс вычисляемого интервала
        end = start + numbers_per_task - 1  # последний индекс вычисляемого интервала
        tasks.append(calculate_sum(start, end))  # добавляем к списку асинхронную функцию подсчета

    results = await asyncio.gather(*tasks)  # ожидаем выполнения всех заданий асинхронно
    total_sum = sum(results)  # считаем сумму тех 5 сумм
    end_time = time()

    print(f"Сумма: {total_sum}")
    print(f"Время выполнения: {end_time - start_time}")


if __name__ == "__main__":
    asyncio.run(main())
```
![async1.png](src%2Fasync1.png)

### multiprocessing1.py
Создаем нужное количество процессов и делим 1_000_000 на количество процессов. Каждый процесс имеет свои ресурсы, в отличие от потоков - нужно создать общий объект Queue, который хранит все суммы. 
Процесс выполнит функцию, которая суммирует все точки данного отрезка и результат добавит в очередь.
После выполнения всех процессов суммируются результаты и выводится в консоли вместе с временем выполнения.
```python
from multiprocessing import Process, Queue
from time import time


def calculate_sum(start, end, queue):
    # queue - очередь значений, куда мы складываем все подсчитанные суммы
    queue.put(sum(range(start, end + 1)))


def main():
    start_time = time()  # засекаем начальное время
    queue = Queue()  # создаем очередь для асинхронного сохранения значений
    process_count = 5  # выполняться программа будет в 5 процессов
    numbers_per_process = 1_000_000 // process_count  # в каждом процессе будет считаться сумма 200_000 чисел
    processes = list()

    for i in range(process_count):
        start = i * numbers_per_process + 1  # первый индекс вычисляемого интервала
        end = start + numbers_per_process - 1  # последний индекс вычисляемого интервала
        p = Process(target=calculate_sum, args=(start, end, queue))  # создаем процесс, передаем функцию и ее параметры
        processes.append(p)  # включаем процесс в наш список, чтобы потом ждать его завершения
        p.start()

    for p in processes:  # в цикле ожидаем завершения всех процессов
        p.join()  # "присоединияемся" к ожиданию окончания

    total_sum = 0  # объявляем общую сумму
    while not queue.empty():  # пока очередь не пуста и в ней есть значения
        total_sum += queue.get()  # складываем с общей суммой

    end_time = time()
    print(f"Сумма: {total_sum}")
    print(f"Время выполнения: {end_time - start_time}")


if __name__ == "__main__":
    main()
```
![multiprocessing1.png](src%2Fmultiprocessing1.png)

### threading1.py
Создаем нужное количество потоков и делим 1_000_000 на количество потоков. Каждый поток выполнит функцию, которая суммирует все точки данного отрезка и результат добавит в лист.
После выполнения всех потоков суммируются результаты и выводится в консоли вместе с временем выполнения.
```python
import threading
from time import time


def calculate_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))
    # в result хранятся последовательно 5 сумм, которые вычисляются параллельно


def main():
    start_time = time()
    thread_count = 5  # выполняться программа будет в 5 потоков
    numbers_per_thread = 1_000_000 // thread_count  # в каждом потоке будет считаться сумма 200_000 чисел
    threads = list()
    results = [0] * thread_count

    for i in range(thread_count):
        start = i * numbers_per_thread + 1  # первый индекс вычисляемого интервала
        end = start + numbers_per_thread - 1  # последний индекс вычисляемого интервала
        t = threading.Thread(target=calculate_sum, args=(start, end, results, i))  # создаем поток, передаем функцию и ее параметры
        threads.append(t)
        t.start()

    for t in threads:  # в цикле ожидаем завершения всех потоков
        t.join()  # "присоединияемся" к ожиданию окончания

    total_sum = sum(results)
    end_time = time()
    print(f"Сумма: {total_sum}")
    print(f"Время выполнения: {end_time - start_time}")


if __name__ == "__main__":
    main()
```
![threading1.png](src%2Fthreading1.png)

### async2.py
```python
import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup
from connection import DBConn
from data import URLs, number_of_threads


async def parse_and_save_async(url, db_conn):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:  # асинхронно создаем клиент-сессию для совершения запросов
            async with session.get(url) as response:  # асинхронно получаем ответ по ссылке из клиента-сессии
                page = await response.text()
                soup = BeautifulSoup(page, 'html.parser')  # создаем парсер
                articles = soup.find_all('article', class_='tm-articles-list__item')
                for article in articles:
                    author = article.find('a', class_='tm-user-info__username').text
                    datetime = article.find('a',
                                            class_='tm-article-datetime-published tm-article-datetime-published_link').text
                    title = article.find('a', class_='tm-title__link').text

                    with db_conn.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                        cursor.execute(DBConn.INSERT_SQL, (title, author, datetime))

                db_conn.commit()
    except Exception as e:
        print("Ошибка:", e)
        db_conn.rollback()


async def process_url_list_async(url_list, conn):
    tasks = []  # создаем список корутин, где будут они храниться
    for url in url_list:
        task = asyncio.create_task(parse_and_save_async(url, conn))
        tasks.append(task)
    await asyncio.gather(*tasks)  # ожидаем выполнения всех заданий асинхронно


async def main():
    chunk_size = len(URLs) // number_of_threads  # определяем количество ссылок для каждой потока (2)
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]  # определяем сами ссылки

    db_conn = DBConn.connect_to_database()

    await asyncio.gather(*(process_url_list_async(chunk, db_conn) for chunk in url_chunks))
    # ожидаем выполнения всех заданий асинхронно

    db_conn.close()


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Время выполнения async: {end_time - start_time} секунд")
```
![async2.png](src%2Fasync2.png)

### multiprocessing2.py
```python
import multiprocessing
import time
import requests
from bs4 import BeautifulSoup
from connection import DBConn
from data import URLs, number_of_threads


def parse_and_save_multiprocessing(url):
    db_conn = DBConn.connect_to_database()
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')  # создаем парсер
        articles = soup.find_all('article', class_='tm-articles-list__item')
        for article in articles:
            author = article.find('a', class_='tm-user-info__username').text
            datetime = article.find('a', class_='tm-article-datetime-published tm-article-datetime-published_link').text
            title = article.find('a', class_='tm-title__link').text

            with db_conn.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                cursor.execute(DBConn.INSERT_SQL, (title, author, datetime))

        db_conn.commit()
    except Exception as e:
        print("Ошибка:", e)
        db_conn.rollback()
    finally:
        db_conn.close()


def process_url_list_multiprocessing(url_list):
    for url in url_list:
        parse_and_save_multiprocessing(url)


def main_multiprocessing():
    chunk_size = len(URLs) // number_of_threads
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]

    processes = []
    for chunk in url_chunks:
        process = multiprocessing.Process(target=process_url_list_multiprocessing, args=(chunk,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
    start_time = time.time()
    main_multiprocessing()
    end_time = time.time()
    print(f"Время выполнения multiprocessing: {end_time - start_time} секунд")
```
![multiprocessing2.png](src%2Fmultiprocessing2.png)

### threading2.py
```python
import threading
import time
from connection import DBConn
import requests
from bs4 import BeautifulSoup
from data import URLs, number_of_threads


def parse_and_save_threading(url, db_conn):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')  # создаем парсер
        articles = soup.find_all('article', class_='tm-articles-list__item')
        for article in articles:
            author = article.find('a', class_='tm-user-info__username').text
            datetime = article.find('a', class_='tm-article-datetime-published tm-article-datetime-published_link').text
            title = article.find('a', class_='tm-title__link').text

            with db_conn.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                cursor.execute(DBConn.INSERT_SQL, (title, author, datetime))

        db_conn.commit()
    except Exception as e:
        print("Ошибка:", e)
        db_conn.rollback()


def process_url_list_threading(url_list, db_conn):
    for url in url_list:  # в цикле берем каждую ссылку
        parse_and_save_threading(url, db_conn)  # и вызываем функцию парсинга


def main_threading():
    chunk_size = len(URLs) // number_of_threads  # определяем количество ссылок для каждого потока (2)
    url_chunks = [URLs[i:i + chunk_size] for i in range(0, len(URLs), chunk_size)]  # определяем сами ссылки

    db_conn = DBConn.connect_to_database()

    threads = []
    for chunk in url_chunks:
        thread = threading.Thread(target=process_url_list_threading, args=(chunk, db_conn))
        threads.append(thread)
        thread.start()

    for thread in threads:  # в цикле всех потоков
        thread.join()  # ожидаем его завершения

    db_conn.close()


if __name__ == '__main__':
    start_time = time.time()
    main_threading()
    end_time = time.time()
    print(f"Время выполнения threading: {end_time - start_time} секунд")
```
![threading2.png](src%2Fthreading2.png)

### data.py
```python
# Список всех ссылок, по которым мы будем собирать данные
URLs = [
    'https://habr.com/ru/flows/develop/articles/',
    'https://habr.com/ru/flows/develop/articles/page2/',
    'https://habr.com/ru/flows/develop/articles/page3/',
    'https://habr.com/ru/flows/develop/articles/page4/',
]

# Количество потоков/единиц выполнения
number_of_threads = 2
```

### connection.py
```python
import psycopg2

class DBConn:
    # SQL команда для вставки книг, %s будут заменять на переданные параметры
    INSERT_SQL = """INSERT INTO public.articles(title, author, datetime) VALUES (%s, %s, %s)"""
    # таблица содержит все поля с типом text
    # Аннотация/декоратор статического метода - метод, который не привязан к состоянию экземпляра или класса
    # (не нужна ссылка на сам класс 'self')
    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname="web_articles_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return conn
```
![db_screenshot.png](src%2Fdb_screenshot.png)

