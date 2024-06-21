# Задача 2:

Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

## Подготовка

Для работы с базой данных подготовим dockerfile который развернет нам postgres.

### Dockerfile

```Dockerfile
FROM postgres:13

ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=database

EXPOSE 5432

CMD ["postgres"]
```

Далее, зададим схему модели бд

### database.py

```python
from sqlmodel import SQLModel, Field, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/database")

engine = create_engine(DATABASE_URL)

class WebPage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    title: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

И доработаем ранее написанный код таким образом, чтобы посредством библиотеки BeautifulSoup код парсил заголовки веб-сайтов. А в main.py позволим в качестве аргумента передавать массив ссылок на сайты, которые необходимо спарсить. Все результаты будем сохранять в postgreSQL

### asyncCode.py

```python
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from sqlmodel import Session
from database import WebPage, create_db_and_tables, engine
import sys

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_and_save(url, session):
    try:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'

        with Session(engine) as db_session:
            webpage = WebPage(url=url, title=title)
            db_session.add(webpage)
            db_session.commit()
    except Exception as e:
        print(f"Ошибка парсинга {url}: {e}")

async def main(urls):
    create_db_and_tables()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(parse_and_save(url, session))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import time
    urls = sys.argv[1:]
    if not urls:
        print("Не предоставлены url для парсинга")
        sys.exit(1)
    start_time = time.time()
    asyncio.run(main(urls))
    end_time = time.time()
    print(f"Async/await занял: {end_time - start_time} секунд")
```

### multiprocessingCode.py

```python
import multiprocessing
import requests
from bs4 import BeautifulSoup
from sqlmodel import Session
from database import WebPage, create_db_and_tables, engine
import sys

def parse_and_save(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'

        with Session(engine) as session:
            webpage = WebPage(url=url, title=title)
            session.add(webpage)
            session.commit()
    except Exception as e:
        print(f"Ошибка парсинга {url}: {e}")

def worker(urls):
    for url in urls:
        parse_and_save(url)

def main(urls):
    num_processes = 4
    create_db_and_tables()
    processes = []
    for i in range(num_processes):
        part = urls[i::num_processes]
        process = multiprocessing.Process(target=worker, args=(part,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    import time
    urls = sys.argv[1:]
    if not urls:
        print("Не предоставлены url для парсинга")
        sys.exit(1)
    start_time = time.time()
    main(urls)
    end_time = time.time()
    print(f"Multiprocessing занял: {end_time - start_time} секунд")
```

### threadingCode.py

```python
import threading
import requests
from bs4 import BeautifulSoup
from sqlmodel import Session
from database import WebPage, create_db_and_tables, engine
import sys

def parse_and_save(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'

        with Session(engine) as session:
            webpage = WebPage(url=url, title=title)
            session.add(webpage)
            session.commit()
    except Exception as e:
        print(f"Ошибка парсинга {url}: {e}")

def worker(urls):
    for url in urls:
        parse_and_save(url)

def main(urls):
    num_threads = 4
    create_db_and_tables()
    threads = []
    for i in range(num_threads):
        part = urls[i::num_threads]
        thread = threading.Thread(target=worker, args=(part,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    import time
    urls = sys.argv[1:]
    if not urls:
        print("Не предоставлены url для парсинга")
        sys.exit(1)
    start_time = time.time()
    main(urls)
    end_time = time.time()
    print(f"Threading занял: {end_time - start_time} секунд")
```

### main.py

```python
import subprocess
import pandas as pd
import sys

def run_program(command, urls):
    try:
        result = subprocess.run(command + urls, capture_output=True, text=True, check=True)
        output = result.stdout.strip().split("\n")
        print(f"{command}: {result.stdout}")
        if "занял" not in output[-1]:
            print(f"Ошибка: {result.stdout}")
            return None
        time_taken = float(output[-1].split(": ")[1].split(" ")[0])
        return time_taken
    except subprocess.CalledProcessError as e:
        print(f"Ошибка запуска команды: {command}: {e.stderr}")
        return None

def main(urls):
    methods = {
        "Threading": ["python3", "threadingCode.py"],
        "Multiprocessing": ["python3", "multiprocessingCode.py"],
        "Async/await": ["python3", "asyncCode.py"]
    }

    results = []

    for method, command in methods.items():
        time_taken = run_program(command, urls)
        if time_taken is not None:
            results.append([method, time_taken])

    df = pd.DataFrame(results, columns=["Method", "Time Taken (s)"])
    print(df)

if __name__ == "__main__":
    urls = sys.argv[1:]  # Список URL для парсинга
    if not urls:
        urls = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.youtube.com",
    "https://www.amazon.com",
    "https://www.wikipedia.org",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.netflix.com",
    "https://www.github.com"
        ]
        print("Выбран дефолтный набор URL", urls)
    main(urls)
```

## Тестирование

Протестируем код при небольшом массиве ссылок

```python
 urls = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.youtube.com",
    "https://www.amazon.com",
    "https://www.wikipedia.org",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.netflix.com",
    "https://www.github.com"
        ]
```

Получим следующие результаты при 4 экземплярах:

| Method          | Result             | Time Taken (s) |
| --------------- | ------------------ | -------------- |
| Threading       | 500000000500000000 | 2.513170       |
| Multiprocessing | 500000000500000000 | 2.554245       |
| Async/await     | 500000000500000000 | 1.364348       |

И такие результаты при 10 экземплярах:

| Method          | Result             | Time Taken (s) |
| --------------- | ------------------ | -------------- |
| Threading       | 500000000500000000 | 1.313953       |
| Multiprocessing | 500000000500000000 | 1.923786       |
| Async/await     | 500000000500000000 | 1.386687       |

Расширим массив ссылок до 30, протестируем код ещё раз

```python
 urls = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.youtube.com",
    "https://www.amazon.com",
    "https://www.wikipedia.org",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.netflix.com",
    "https://www.github.com",
    "https://www.apple.com",
    "https://www.microsoft.com",
    "https://www.reddit.com",
    "https://www.twitch.tv",
    "https://www.ebay.com",
    "https://www.pinterest.com",
    "https://www.paypal.com",
    "https://www.stackoverflow.com",
    "https://www.wordpress.com",
    "https://www.quora.com",
    "https://www.bing.com",
    "https://www.yelp.com",
    "https://www.dropbox.com",
    "https://www.soundcloud.com",
    "https://www.spotify.com",
    "https://www.tumblr.com",
    "https://www.adobe.com",
    "https://www.medium.com",
    "https://www.bbc.com",
    "https://www.nytimes.com",
    "https://www.cnn.com"
]
```

Получим следующие результаты при 4 экземплярах:

| Method          | Result             | Time Taken (s) |
| --------------- | ------------------ | -------------- |
| Threading       | 500000000500000000 | 4.975893       |
| Multiprocessing | 500000000500000000 | 4.516615       |
| Async/await     | 500000000500000000 | 1.628181       |

И следующие результаты при 10 экземплярах:

| Method          | Result             | Time Taken (s) |
| --------------- | ------------------ | -------------- |
| Threading       | 500000000500000000 | 2.590408       |
| Multiprocessing | 500000000500000000 | 2.872148       |
| Async/await     | 500000000500000000 | 1.440655       |

## Итоги

Лучше всего себя показывает async/await. Однако, при увеличении числа потоков, threading и multiprocessing наступают ему на пятки. Это связано с тем, что в данной задаче нет никаких ресурсоемких процессов и async/await подход позволяет одновременно отправить запрос для парсинга на столько сайтов, на сколько это потребуется. В свою очередь threading и multiprocessing отправляют запросы на парсинг по одному, поэтому, не успевают за async/await. Как итог, для задач связанных с http запросами async/await подходит лучше всего
