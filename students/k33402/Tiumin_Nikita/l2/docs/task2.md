# Задание 2

*Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.*

## parse_threading.py

```python
from multiprocessing.pool import ThreadPool
from time import time
from db import get_connnection, close_connection, create_trip, insert_trip
from parser import parse_trips


RUNS_NUMBER = 3
CHUNKS_NUMBER = 4
PAGES_NUMBER = 16


def parse_and_save(urls):
    parsed_trips = []
    for url in urls:
        next_parsed_trips = parse_trips(url)
        parsed_trips = [*parsed_trips, *next_parsed_trips]

    conn = get_connnection()
    for trip in parsed_trips:
        trip_to_insert = create_trip(trip)
        insert_trip(conn, trip_to_insert)
    close_connection(conn)
    return 'success'


def main():
    args = []
    base_url = 'https://bolshayastrana.com/tury?plainSearch=1&page='
    urls = [base_url + str(i + 1) for i in range(PAGES_NUMBER)]

    for i in range(CHUNKS_NUMBER):
        chunk_len = len(urls) / CHUNKS_NUMBER
        args.append(urls[int(i*chunk_len):int((i+1)*chunk_len)])

    pool = ThreadPool(len(args))

    start = time()
    res = pool.map(parse_and_save, args)
    pool.close()
    pool.join()
    exec_time = time() - start

    return exec_time, res


if __name__ == "__main__":
    times = []
    for i in range(RUNS_NUMBER):
        next_time, res = main()
        times.append(next_time)
        print(i + 1, ' run: ', next_time, 's. RESULT: ', res)
    print('Average time: ', sum(times) / len(times), 's')
```

## parse_multiprocessing.py

```python
import multiprocessing
from time import time
from db import get_connnection, close_connection, create_trip, insert_trip
from parser import parse_trips


RUNS_NUMBER = 3
CHUNKS_NUMBER = 4
PAGES_NUMBER = 16


def parse_and_save(urls):
    parsed_trips = []
    for url in urls:
        next_parsed_trips = parse_trips(url)
        parsed_trips = [*parsed_trips, *next_parsed_trips]

    conn = get_connnection()
    for trip in parsed_trips:
        trip_to_insert = create_trip(trip)
        insert_trip(conn, trip_to_insert)
    close_connection(conn)
    return 'success'


def main():
    args = []
    base_url = 'https://bolshayastrana.com/tury?plainSearch=1&page='
    urls = [base_url + str(i + 1) for i in range(PAGES_NUMBER)]

    for i in range(CHUNKS_NUMBER):
        chunk_len = len(urls) / CHUNKS_NUMBER
        args.append(urls[int(i*chunk_len):int((i+1)*chunk_len)])

    pool = multiprocessing.Pool(len(args))

    start = time()
    res = pool.map(parse_and_save, args)
    pool.close()
    pool.join()
    exec_time = time() - start

    return exec_time, res


if __name__ == "__main__":
    times = []
    for i in range(RUNS_NUMBER):
        next_time, res = main()
        times.append(next_time)
        print(i + 1, ' run: ', next_time, 's. RESULT: ', res)
    print('Average time: ', sum(times) / len(times), 's')
```

## parse_asyncio.py

```python
import asyncio
from time import time
from db import get_connnection, close_connection, create_trip, insert_trip
from parser import parse_trips


RUNS_NUMBER = 3
CHUNKS_NUMBER = 4
PAGES_NUMBER = 16


async def parse_and_save(urls):
    parsed_trips = []
    for url in urls:
        next_parsed_trips = parse_trips(url)
        parsed_trips = [*parsed_trips, *next_parsed_trips]

    conn = get_connnection()
    for trip in parsed_trips:
        trip_to_insert = create_trip(trip)
        insert_trip(conn, trip_to_insert)
    close_connection(conn)
    return 'success'


async def main():
    tasks = []
    base_url = 'https://bolshayastrana.com/tury?plainSearch=1&page='
    urls = [base_url + str(i + 1) for i in range(PAGES_NUMBER)]

    for i in range(CHUNKS_NUMBER):
        chunk_len = len(urls) / CHUNKS_NUMBER
        task = asyncio.create_task(parse_and_save(urls[int(i*chunk_len):int((i+1)*chunk_len)]))
        tasks.append(task)

    start = time()
    res = await asyncio.gather(*tasks)
    exec_time = time() - start

    return exec_time, res


if __name__ == "__main__":
    times = []
    for i in range(RUNS_NUMBER):
        next_time, res = asyncio.run(main())
        times.append(next_time)
        print(i + 1, ' run: ', next_time, 's. RESULT: ', res)
    print('Average time: ', sum(times) / len(times), 's')
```

## Выводы

|             | **Threading** | **Multiprocessing** | **Asyncio** |
| ----------- | ----------- | ----------------- | ------------- |
| 1           | 8.34       | 6.60             | 8.91       |
| 2           | 8.98       | 7.11             | 13.57       |
| 3           | 7.40       | 7.80             | 13.35       |
| **Avg**     | 8.24       | 7.17             | 11.94       |

- **Threading**: Продемонстрировал время выполнения сравнимое с мультипроцессорностью.
- **Multiprocessing**: Подход показал наилучшие показатели. Это связано с разделением обработки и ззаписи данных на несколько процессов
- **Asyncio**: Наиболее медленный 