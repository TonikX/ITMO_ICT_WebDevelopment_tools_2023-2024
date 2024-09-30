#Лабораторная работа - 2

###Задание - 1

Написать три различных программы на Python, использующие каждый из подходов: threading, 
multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. 
Разделите вычисления на несколько параллельных задач для ускорения выполнения.

####threading

``` py
import threading
import time

def calculate_sum(start, finish, result_list, index):
    total = 0
    for i in range(start, finish + 1):
        total += i
    result_list[index] = total

def threading_count():
    threads = []
    chunks = 5
    total = 1000000
    chunk_size = total // chunks
    results = [0] * chunks

    start_time = time.time()
    for i in range(chunks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    final_result = sum(results)

    print(f"Result: {final_result}")
    print(f"Threading time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    threading_count()
```
    Описание работы -  реализуем многопоточность через threading создавая несколько потоков в одном процессе
    
####multiprocessing

``` py
import multiprocessing
import time

def calculate_sum(start, finish, result_list, index):
    total = 0
    for i in range(start, finish + 1):
        total += i
    result_list[index] = total  # Сохраняем результат в общий список

def multiprocessing_count():
    processes = []
    chunks = 5
    total = 1000000
    chunk_size = total // chunks

    # Используем Manager для создания списка, который может быть разделен между процессами
    with multiprocessing.Manager() as manager:
        results = manager.list([0] * chunks)

        start_time = time.time()
        for i in range(chunks):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size
            process = multiprocessing.Process(target=calculate_sum, args=(start, end, results, i))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()

        final_result = sum(results)
        print(f"Result: {final_result}")
        print(f"Multiprocessing time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    multiprocessing_count()
```
Описание работы - реализуем одновременное выполнение через отдельные процессы

####async

``` py
import asyncio
import time

def calculate_sum(start, finish, result_list, index):
    total = 0
    for i in range(start, finish + 1):
        total += i
    result_list[index] = total

async def async_calculate_sum(start, end, result_list, index):
    calculate_sum(start, end, result_list, index)

async def asyncio_example():
    tasks = []
    chunks = 5
    total = 1000000
    chunk_size = total // chunks
    results = [0] * chunks

    start_time = time.time()
    for i in range(chunks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        task = asyncio.create_task(async_calculate_sum(start, end, results, i))
        tasks.append(task)

    await asyncio.gather(*tasks)
    end_time = time.time()

    final_result = sum(results)
    print(f"Result: {final_result}")
    print(f"Asyncio time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(asyncio_example())
```
Описание работы -  реализуем мультипоточность через async приостанавливая выполнение процессов и возращаясь к ним потом


####Вывод

Время

- threading - 0.0470сек

- multiprocessing - 0.2260сек

- async - 0.0406сек

Threading лучше всего подходит для I/O-ориентированных задач, но ограничен GIL.

Multiprocessing идеален для CPU-ориентированных задач и не подвержен GIL, но требует больше ресурсов. 

Async предоставляет эффективный способ обработки I/O без блокировок, но не подходит для задач, требующих интенсивных вычислений.


###Задание - 2

Напиcать программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных 
с использованием подходов threading, multiprocessing и async.
Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

####threading
```py
import threading
import requests
from bs4 import BeautifulSoup
import time
from database import get_session, Site, init_db

init_db() 

def parse_and_save(url):
    session = get_session()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    site = Site(url=url, title=title, method='GET')
    session.add(site)
    session.commit()
    session.close()
    print(f"{url} - {title}")

def threading_example():
    urls = [
        'https://www.example.com',
        'https://www.google.com',
        'https://www.python.org',
        'https://www.stackoverflow.com',
        'https://www.github.com'
    ]
    threads = []

    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_time = time.time()
    threading_example()
    end_time = time.time()
    print(f"Threading time: {end_time - start_time:.4f} seconds")
```

####multiprocessing
```py
import multiprocessing
import requests
from bs4 import BeautifulSoup
import time
from database import get_session, Site, init_db

init_db()  # Initialize the database

def parse_and_save(url):
    session = get_session()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    site = Site(url=url, title=title, method='GET')
    session.add(site)
    session.commit()
    session.close()
    print(f"{url} - {title}")

def multiprocessing_example():
    urls = [
        'https://www.example.com',
        'https://www.google.com',
        'https://www.python.org',
        'https://www.stackoverflow.com',
        'https://www.github.com'
    ]

    with multiprocessing.Pool() as pool:
        pool.map(parse_and_save, urls)

if __name__ == "__main__":
    start_time = time.time()
    multiprocessing_example()
    end_time = time.time()
    print(f"Multiprocessing time: {end_time - start_time:.4f} seconds")
```

####async
```py
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
from database import get_session, Site, init_db

init_db()

async def parse_and_save_async(url: str) -> None:
    async with aiohttp.ClientSession() as session:
            response = await fetch_page(session, url)
            soup = BeautifulSoup(response, 'html.parser')
            title = soup.title.string
            session = get_session()
            site = Site(url=url, title=title, method='async')
            session.add(site)
            session.commit()
            session.refresh(site)

            print(f"{url} - {title}")


async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, ssl=False) as response:
        return await response.text()

async def asyncio_example():
    urls = [
        'https://www.example.com',
        'https://www.google.com',
        'https://www.python.org',
        'https://www.stackoverflow.com',
        'https://www.github.com'
    ]

    tasks = [parse_and_save_async(url) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(asyncio_example())
    end_time = time.time()
    print(f"Asyncio time: {end_time - start_time:.4f} seconds")
```

####database
```py 
from sqlmodel import SQLModel, create_engine, Session, Field

db_url = 'postgresql://postgres:123@localhost/db_lab2'
engine = create_engine(db_url, echo=False)

class Site(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str
    title: str
    method: str

def get_session() -> Session:
    return Session(bind=engine)

def init_db():
    SQLModel.metadata.create_all(engine)
```

####Вывод

![Задача](assets/lab2/a.PNG)

Время

- threading - 0.6671 сек

- multiprocessing - 3.3805 сек

- async - 0.7907 сек

Задача для сравнения разных методов разделения работы, но на таком примере мы можем увидеть, что для маленького
обьема информации нет смысла использовать multiprocessing и при этом по очевидным причинам treading несколько быстрее
чем async