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
- **1-е время исполнения:** 2.2885212898254395
- **2-е время исполнения:** 2.4867148399353027
- **3-е время исполнения:** 2.6772518157958984

## Выводы

|             | **Threading** | **Multiprocessing** | **Asyncio** |
| ----------- | ----------- | ----------------- | ------------- |
| 1           | 1.748       | 2.991             | 2.289       |
| 2           | 1.345       | 2.358             | 2.487       |
| 3           | 1.265       | 2.353             | 2.677       |
| **Avg**     | 1.452       | 2.567             | 2.484       |

- **Threading**: продемонстрировала самое быстрое среднее время выполнения, вероятно, из-за ее легкости и способности распределять память между потоками, что ускоряет задачи, связанные с вводом-выводом, такие как веб-анализ.
- **Multiprocessing**: этот подход имел самое медленное среднее время выполнения, возможно, из-за накладных расходов, связанных с созданием нескольких процессов и управлением ими. Хотя многопроцессорная обработка
- **Asyncio**: этот подход имел немного более быстрое среднее время выполнения, чем многопроцессорный, но медленнее, чем многопоточный (2,484 секунды). Хотя asyncio предназначен для эффективной обработки задач, связанных с вводом-выводом, за счет использования одного потока и неблокирующих операций ввода-вывода, в этом сценарии он мог бы повлечь за собой накладные расходы из-за управления циклом событий или специфического характера выполняемых задач.