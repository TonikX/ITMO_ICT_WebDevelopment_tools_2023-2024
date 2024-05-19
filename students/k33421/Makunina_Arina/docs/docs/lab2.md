# Лабораторная работа №2: Сравнение подходов к параллельному программированию в Python

В данной лабораторной работе мы сравниваем три различных подхода к параллельному программированию в Python: threading, multiprocessing и async. 

Задача 1: Каждый из подходов используется для решения задачи суммирования всех чисел от 1 до 1000000, разбивая вычисления на несколько параллельных задач для ускорения выполнения.

## Threading

Первый подход использует модуль `threading` для создания нескольких потоков, каждый из которых выполняет часть вычислений. Код программы `thread.py` выглядит следующим образом:
```python
import threading
from time import time

def calculate_sum(start, end, result, index):
    total = sum(range(start, end + 1))
    result[index] = total

def main():
    thread_count = 10
    numbers_per_thread = 100000 // thread_count
    threads = []
    results = [0] * thread_count

    start_time = time()
    for i in range(thread_count):
        start = i * numbers_per_thread + 1
        end = start + numbers_per_thread - 1
        t = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_sum = sum(results)
    print(f"Total sum is {total_sum}")

    end_time = time()
    print(f"Threading time: {end_time - start_time}")

if __name__ == "__main__":
    main()
```
Время выполнения программы: 0.004998922348022461 сек.

## Multiprocessing

Второй подход использует модуль `multiprocessing` для создания нескольких процессов, каждый из которых выполняет часть вычислений. Код программы `multi.py` выглядит следующим образом:
```python
from multiprocessing import Process, Array
from time import time

def calculate_sum(start, end, result, index):
    total = sum(range(start, end + 1))
    result[index] = total

def main():
    process_count = 10
    numbers_per_process = 100000 // process_count
    processes = []
    results = Array("i", process_count)

    start_time = time()
    for i in range(process_count):
        start = i * numbers_per_process + 1
        end = start + numbers_per_process - 1
        p = Process(target=calculate_sum, args=(start, end, results, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total_sum = sum(results)
    print(f"Total sum is {total_sum}")

    end_time = time()
    print(f"Multiprocessing time: {end_time - start_time}")

if __name__ == "__main__":
    main()
```
Время выполнения программы: 0.35558557510375977 сек.

## Async

Третий подход использует модуль `asyncio` для создания нескольких асинхронных задач, каждая из которых выполняет часть вычислений. Код программы `asyn.py` выглядит следующим образом:
```python
import asyncio
from time import time

async def calculate_sum(start, end):
    total = sum(range(start, end + 1))
    return total

async def main():
    task_count = 10
    numbers_per_task = 100000 // task_count
    tasks = []

    start_time = time()
    for i in range(task_count):
        start = i * numbers_per_task + 1
        end = start + numbers_per_task - 1
        tasks.append(calculate_sum(start, end))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    print(f"Total sum is {total_sum}")

    end_time = time()
    print(f"Async time: {end_time - start_time}")

if __name__ == "__main__":
    asyncio.run(main())
```
Время выполнения программы: 0.001003265380859375 сек.

## Сравнение результатов

В таблице ниже приведены результаты сравнения времени выполнения программ на основе разных подходов:

| Approach | Time (sec) |
| --- | --- |
| Threading | 0.004998922348022461 |
| Multiprocessing | 0.35558557510375977 |
| Async | 0.001003265380859375 |

Как видно из таблицы, подход с использованием `asyncio` оказался самым быстрым, что связано с эффективным использованием асинхронных задач для параллельного выполнения вычислений. Подход с использованием `multiprocessing` оказался медленнее, что связано с дополнительными затратами на создание и управление процессами. Подход с использованием `threading` оказался медленнее, чем `asyncio`, но быстрее, чем `multiprocessing`, что связано с ограничениями на использование потоков в Python.

Задача 2: описаны три программы на Python для параллельного парсинга веб-страниц с сохранением данных в базу данных, используя подходы threading, multiprocessing и async.

Threading Approach
--------------------

Программа `threading_parsing.py` использует модуль `threading` для параллельного парсинга веб-страниц. Она создает несколько потоков, каждый из которых парсит информацию с отдельного веб-сайта.

### Код
```python
def parse_data_chunk(urls):
    for url in urls:
        parse_data(url)

def parse_data_in_parallel(urls):
    start_time = datetime.now()

    num_threads = 2
    chunk_size = len(urls) // num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(urls)
        chunk = urls[start:end]
        t = threading.Thread(target=parse_data_chunk, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = datetime.now()
    logging.info(f"Total parsing time: {end_time - start_time}")

urls = [
    "https://status.msk.cloud.vk.com/incidents",
    "https://status.yandex.cloud/ru/timeline",
]

if __name__ == "__main__":
    parse_data_in_parallel(urls)
```
### Результаты
```
Total parsing time: 0:00:15.488683
```
Multiprocessing Approach
-------------------------

Программа `multiprocessing_parsing.py` использует модуль `multiprocessing` для параллельного парсинга веб-страниц. Она создает несколько процессов, каждый из которых парсит информацию с отдельного веб-сайта.

### Код
```python
urls = [
    "https://status.msk.cloud.vk.com/incidents",
    "https://status.yandex.cloud/ru/timeline",
]


def parse_data_in_parallel(urls):
    with multiprocessing.Pool(processes=2) as pool:
        pool.map(parse_data, urls)


if __name__ == "__main__":
    start_time = datetime.now()
    parse_data_in_parallel(urls)
    end_time = datetime.now()
    logging.info(f"All URLs parsed in {end_time - start_time}")
```
### Результаты
```
INFO - All URLs parsed in 0:00:14.994050
```
Async Approach
--------------

Программа `async_parsing.py` использует модуль `aiohttp` и `asyncio` для параллельного парсинга веб-страниц. Она создает несколько задач, каждая из которых парсит информацию с отдельного веб-сайта.

### Код
```python
async def parse_data(session, url):
    logging.info(f"Started scraping site {url}")
    s = Service(
        "C:\\Users\\a.makunina\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    )
    driver = webdriver.Chrome(service=s)

    async with session.get(url):
            driver.get(url)
        ...

async def main():
    urls = [
        "https://status.msk.cloud.vk.com/incidents",
        "https://status.yandex.cloud/ru/timeline",
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [parse_data(session, url) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = datetime.now()
    asyncio.run(main())
    end_time = datetime.now()
    logging.info(f"All URLs parsed in {end_time - start_time}")
```
### Результаты
```
All URLs parsed in 0:00:23.774665
```
Сравнение результатов
-------------------------

| Approach | Time (sec) |
| --- | --- |
| Threading | 0:00:15.488683 |
| Multiprocessing | 0:00:14.994050 |
| Async | 0:00:23.774665 |

Как видно из таблицы, подход с использованием multiprocessing оказался самым быстрым, за ним следует threading, а async подход оказался самым медленным. Это может быть связано с тем, что async подход использует дополнительные ресурсы для создания задач и управления ими, что может привести к дополнительной задержке.

Заключение
----------
Полученные данные подчеркивают, что выбор между threading, multiprocessing, и async подходами должен быть обусловлен спецификой задачи. В частности:

- Для легковесных операций с большим количеством ожидания (IO-bound tasks), таких как запросы к API или операции чтения/записи файлов, предпочтительнее использовать async.
- Для задач, требующих интенсивных вычислений и минимальное взаимодействие с внешними системами (CPU-bound tasks), эффективнее могут быть multiprocessing.
- Threading может быть хорошим компромиссом в ситуациях, когда задачи не требуют интенсивной работы с CPU, но при этом есть необходимость в параллельной обработке данных без значительного оверхеда, связанного с процессами.