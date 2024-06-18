# Задача 2. Параллельный парсинг веб-страниц с сохранением в базу данных

**Задача: Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.**

**Подробности задания:**

- Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async.
- Каждая программа должна содержать функцию parse_and_save(url), которая будет загружать HTML-страницу по указанному URL, парсить ее, сохранять заголовок страницы в базу данных и выводить результат на экран.
- Используйте базу данных из лабораторной работы номер 1 для заполенния ее данными. Если Вы не понимаете, какие таблицы и откуда Вы могли бы заполнить с помощью парсинга, напишите преподавателю в общем чате потока.
- Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова async/await и модуль aiohttp для асинхронных запросов.
- Создайте список нескольких URL-адресов веб-страниц для парсинга и разделите его на равные части для параллельного парсинга.
- Запустите параллельный парсинг для каждой программы и сохраните данные в базу данных.
- Замерьте время выполнения каждой программы и сравните результаты.

**Дополнительные требования:**

- Сделайте документацию, содержащую описание каждой программы, используемые подходы и их особенности.
- Включите в документацию таблицы, отображающие время выполнения каждой программы.
- Прокомментируйте результаты сравнения времени выполнения программ на основе разных подходов.

## Решение

### async.py

```python
import aiohttp
import asyncio
import asyncpg
from bs4 import BeautifulSoup
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import *


async def save_to_db(data):
    conn = await asyncpg.connect("postgresql://postgres:1@localhost:5432/web_data")
    try:
        await conn.execute(
            "INSERT INTO site (url, title) VALUES ($1, $2)", data["url"], data["title"]
        )
    finally:
        await conn.close()


async def get_data(url, session):
    async with session.get(url) as response:
        return await response.text()


async def parse_and_save(url):
    async with aiohttp.ClientSession() as session:

        html = await get_data(url, session)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("title").text
        await save_to_db({"url": url, "title": title})


async def main(urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(parse_and_save(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":

    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(urls))
    end_time = time.time()
    execution_time = end_time - start_time
    file = open("times.txt", "a")

    file.write(f"Async time: {execution_time}\n")

```

### mtlprcs.py

```python
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import *


def parse_and_save(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text

    conn = psycopg2.connect("postgresql://postgres:1@localhost:5432/web_data")
    curs = conn.cursor()

    curs.execute("INSERT INTO site (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()


def main(urls):
    num_process = len(urls) if len(urls) < 4 else 4
    pool = Pool(processes=num_process)
    pool.map(parse_and_save, urls)


if __name__ == "__main__":
    start_time = time.time()
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time
    file = open("times.txt", "a")

    file.write(f"Multiprocessing time: {execution_time}\n")

```

### thrd.py

```python
from threading import Thread
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import *



def parse_and_save(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text

    conn = psycopg2.connect("postgresql://postgres:1@localhost:5432/web_data")
    curs = conn.cursor()

    curs.execute("INSERT INTO site (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()


def main(urls):

    threads = []
    for url in urls:
        thread = Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start_time = time.time()
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time
    file = open("times.txt", "a")

    file.write(f"Threading time: {execution_time}\n")

```

### db.py

```python
from sqlmodel import SQLModel, create_engine, Field, Session
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DB_URL")

engine = create_engine(db_url, echo=True)

def create_database_session() -> Session:
    return Session(bind=engine)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

class Site(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str
    title: str


init_db()
```

### urls.py

```python
urls = [
    'https://career.habr.com/vacancies?qid=1&type=all',
    'https://career.habr.com/vacancies?q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&qid=3&type=all',
    'https://career.habr.com/vacancies?q=python%20&qid=3&type=all',

]
```

### times.txt

```
Async time: 2.4517574310302734
Multiprocessing time: 3.675524950027466
Threading time: 1.6073400974273682
```
