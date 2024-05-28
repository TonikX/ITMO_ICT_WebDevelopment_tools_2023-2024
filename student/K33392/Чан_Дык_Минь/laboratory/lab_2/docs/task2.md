# Задание 2

*Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.*

## threading_parse.py

```python
import threading
import time
from db import init_db, create_trip, TripDefault
from typing import List
from datetime import datetime, date
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore
from urls import URLS


def parse_trip(url: str) -> TripDefault:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string
    date_start = date.today()
    date_end = date.today()
    estimated_cost = soup.find(lambda tag: tag.has_attr('class') and 'price' in tag['class'])
    if estimated_cost:
        estimated_cost = estimated_cost.text.strip()
        estimated_cost = float(''.join(filter(lambda x: x.isdigit() or x == '.', estimated_cost)))
    else:
        estimated_cost = 10000.0

    trip_status = "Threading"
    other_details = "The link to the trip is: " + url
    return TripDefault(
        title=title, 
        date_start=date_start, 
        date_end=date_end, 
        estimated_cost=estimated_cost, 
        trip_status=trip_status, 
        other_details=other_details
        )

def save_trips(urls: List[str]):
    for url in urls:
        trip = parse_trip(url)
        create_trip(trip)
        print(f"Trip saved: {trip}")

def main():
    threads = []
    for url in URLS:
        thread = threading.Thread(target=save_trips, args=(url,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    init_db()
    start_time = time.time()
    main()
    print(f"Execution time using Threading: {time.time() - start_time}")
```
- **1-е время исполнения:** 1.7479641437530518
- **2-е время исполнения:** 1.3483960628509521
- **3-е время исполнения:** 1.2648613452911377

## multiprocessing_parse.py

```python
import multiprocessing
import time
from db import init_db, create_trip, TripDefault
from typing import List
from datetime import datetime, date
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore
from urllib.request import urlopen
from urls import URLS


def parse_trip(url: str) -> TripDefault:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string
    date_start = date.today()
    date_end = date.today()
    estimated_cost = soup.find(lambda tag: tag.has_attr('class') and 'price' in tag['class'])
    if estimated_cost:
        estimated_cost = estimated_cost.text.strip()
        estimated_cost = float(''.join(filter(lambda x: x.isdigit() or x == '.', estimated_cost)))
    else:
        estimated_cost = 10000.0

    trip_status = "Multiprocessing"
    other_details = "The link to the trip is: " + url
    return TripDefault(
        title=title, 
        date_start=date_start, 
        date_end=date_end, 
        estimated_cost=estimated_cost, 
        trip_status=trip_status, 
        other_details=other_details
        )

def save_trips(urls: List[str]):
    for url in urls:
        trip = parse_trip(url)
        create_trip(trip)
        print(f"Trip saved: {trip}")

def main():
    processes = []
    for url in URLS:
        process = multiprocessing.Process(target=save_trips, args=(url,))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()

if __name__ == "__main__":
    init_db()
    start_time = time.time()
    main()
    print(f"Execution time using Multiprocessing: {time.time() - start_time}")
```
- **1-е время исполнения:** 2.9909141063690186
- **2-е время исполнения:** 2.3584067821502686
- **3-е время исполнения:** 2.3532962799072266

## asyncio_parse.py

```python
import asyncio
import time
from db import init_db, create_trip, TripDefault
from typing import List
from datetime import datetime, date
from bs4 import BeautifulSoup # type: ignore
import requests  # type: ignore
from urls import URLS


async def parse_trip(url: str) -> TripDefault:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string
    date_start = date.today()
    date_end = date.today()
    estimated_cost = soup.find(lambda tag: tag.has_attr('class') and 'price' in tag['class'])
    if estimated_cost:
        estimated_cost = estimated_cost.text.strip()
        estimated_cost = float(''.join(filter(lambda x: x.isdigit() or x == '.', estimated_cost)))
    else:
        estimated_cost = 10000.0

    trip_status = "Asyncio"
    other_details = "The link to the trip is: " + url
    return TripDefault(
        title=title, 
        date_start=date_start, 
        date_end=date_end, 
        estimated_cost=estimated_cost, 
        trip_status=trip_status, 
        other_details=other_details
        )

async def save_trips(urls: List[str]):
    for url in urls:
        trip = await parse_trip(url)
        create_trip(trip)
        print(f"Trip saved: {trip}")

async def main():
    tasks = []

    for url in URLS:
        task = asyncio.create_task(save_trips(url))
        tasks.append(task)
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    init_db()
    start_time = time.time()
    asyncio.run(main())
    print(f"Execution time using Asyncio: {time.time() - start_time}")
```
- **1-е время исполнения:** 1.4365535259246826
- **2-е время исполнения:** 1.2479448318481445
- **3-е время исполнения:** 1.439009428024292

## Выводы

|             | **Threading** | **Multiprocessing** | **Asyncio** |
| ----------- | ----------- | ----------------- | ------------- |
| 1           | 1.748       | 2.991             | 1.437       |
| 2           | 1.345       | 2.358             | 1.250       |
| 3           | 1.265       | 2.353             | 1.439       |
| **Avg**     | 1.452       | 2.567             | 1.375       |



1. **Потоки**:
    - Поточный подход показывает относительно хорошую производительность: среднее время выполнения для трех прогонов составляет 1,452 секунды.
    - Потоки легкие и могут эффективно создаваться и управляться операционной системой, что делает их пригодными для задач, связанных с вводом-выводом, таких как очистка веб-страниц.
    - Однако глобальная блокировка интерпретатора (GIL) в Python ограничивает настоящий параллелизм, поскольку одновременно только один поток может выполнять байт-код Python.

2. **Многопроцессорность**:
    - Многопроцессорный подход имеет самую низкую производительность: среднее время выполнения для трех прогонов составляет 2,567 секунды.
    — Хотя многопроцессорность обеспечивает настоящий параллелизм за счет создания отдельных процессов, накладные расходы на создание новых процессов и межпроцессное взаимодействие могут быть значительными, особенно для задач, связанных с вводом-выводом, таких как парсинг веб-страниц.
    — Многопроцессорный подход может быть более подходящим для задач, связанных с ЦП, которые могут выиграть от параллелизма между несколькими ядрами.

3. **Асинхронность**:
    — Подход asyncio показывает наилучшую производительность: среднее время выполнения за три прогона составляет 1,375 секунды.
    - Asyncio использует совместную многозадачность и циклы событий, позволяя эффективно обрабатывать задачи, связанные с вводом-выводом, без затрат на создание нескольких потоков или процессов.
    - Asyncio особенно хорошо подходит для задач, связанных с вводом-выводом, таких как очистка веб-страниц, поскольку он может обрабатывать несколько запросов одновременно, не блокируя цикл событий.

Подводя итог, можно сказать, что для данной задачи парсинга веб-страниц подход asyncio кажется наиболее эффективным, за ним следует подход многопоточности. Многопроцессорный подход, хотя и обеспечивает настоящий параллелизм, влечет за собой значительные накладные расходы и может быть не лучшим выбором для этой конкретной задачи, связанной с вводом-выводом.