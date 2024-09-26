# Лабораторная 2

## Задание 1

### Thread

```python
import threading
import time

RESULTS = []

def calculate_sum(part_id, part, ts, total_numbers):
        start = part_id * part + 1
        end = (part_id + 1) * part if part_id != (ts - 1) else total_numbers
        global RESULTS
        RESULTS[part_id] = sum(range(start, end + 1))

def main_threading(total_numbers=1000000, ts=4):
    threads = []
    global RESULTS
    RESULTS = [0] * ts
    part = total_numbers // ts

    for i in range(ts):
        thread = threading.Thread(target=calculate_sum, args=(i, part, ts, total_numbers))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(RESULTS)
    print(f"Total sum is: {total_sum}")


if __name__ == "__main__":
    start_time = time.perf_counter()
    main_threading()
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time} секунд")
```

### Multiprocess

```python
from multiprocessing import Process, Queue
import time


def calculate_sum(start, end, results):
    results.put(sum(range(start, end + 1)))


def main_multiprocessing(total_numbers=1000000, ts=4):
    results = Queue()
    processes = []
    part = total_numbers // ts

    for i in range(ts):
        start = i * part + 1
        end = (i + 1) * part if i != ts - 1 else total_numbers
        process = Process(target=calculate_sum, args=(start, end, results))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    total_sum = 0
    while not results.empty():
        total_sum += results.get()

    print(f"Total sum is: {total_sum}")


if __name__ == "__main__":
    start_time = time.perf_counter()
    main_multiprocessing()
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time} секунд")
```


### Async

```python
import asyncio
import time


async def calculate_sum_async(start, end):
    return sum(range(start, end + 1))


async def main_async(total_numbers=1000000, ts=4):
    part = total_numbers // ts
    threads = []

    for i in range(ts):
        start = i * part + 1
        end = (i + 1) * part if i != ts-1 else total_numbers
        threads.append(calculate_sum_async(start, end))

    results = await asyncio.gather(*threads)
    total_sum = sum(results)
    print(f"Total sum is: {total_sum}")


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main_async())
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time} секунд")
```

## Задание 2


### Async

```python
import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def parse_and_save(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text if soup.find('title') else 'No title found'
        print(f'Processed {url}: {title}')
        # Сохранение в базу данных, аналогично threading

async def main_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)

urls = []
asyncio.run(main_async(urls))
```

### Thread

```python
import threading
import requests
from bs4 import BeautifulSoup
import psycopg2


def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text

    conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/labs')
    curs = conn.cursor()

    curs.execute("INSERT INTO site (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()


def main_threading(urls):
    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


urls = []
main_threading(urls)
```

### Multiprocess

```python
from multiprocessing import Process
import requests
from bs4 import BeautifulSoup
import psycopg2

def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text

    conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/labs')
    curs = conn.cursor()

    curs.execute("INSERT INTO site (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()

def main_multiprocessing(urls):
    processes = []
    for url in urls:
        process = Process(target=parse_and_save, args=(url))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

urls = []
main_multiprocessing(urls)
```


## Результаты

    | Solution      | Time (seconds)     |
    |---------------|--------------------|
    | Async         | 1.2993099689483643 |
    | Multiprocess  | 1.6727426052093506 |
    | Threading     | 1.244816780090332  |



    | Solution      | Time (seconds)     |
    |---------------|--------------------|
    | Async         | 0.35082180000608787 |
    | Multiprocess  | 0.9894510000012815 |
    | Threading     | 0.504782800009707  |