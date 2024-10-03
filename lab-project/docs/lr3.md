# Лабораторная работа №3

## Задание
Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с базой данных и вызывать парсер через API и очередь.

Задачи 1 и 2 - задачи на минимум для сдачи - 70% баллов. Задачи 1, 2 и 3 - 100% баллов.

### Подзадача 1: Упаковка FastAPI приложения, базы данных и парсера данных в Docker
Docker — это платформа для разработки, доставки и запуска приложений в контейнерах. Контейнеры позволяют упаковать приложение и все его зависимости в единый образ, который можно запускать на любой системе, поддерживающей Docker, что обеспечивает консистентность среды выполнения и упрощает развертывание. Docker помогает ускорить разработку, повысить гибкость и масштабируемость приложений. Материалы: [Основы работы с Docker](https://tproger.ru/translations/docker-for-beginners/.

Создание FastAPI приложения: Создано в рамках лабораторной работы номер 1

Создание базы данных: Создано в рамках лабораторной работы номер 1

Создание парсера данных: Создано в рамках лабораторной работы номер 2

Реулизуйте возможность вызова парсера по http Для этого можно сделать отдельное приложение FastAPI для парсера или воспользоваться библиотекой socket или подобными.

### Подзадача 2: Вызов парсера из FastAPI
** Эндпоинт в FastAPI для вызова парсера**:
Необходимо добавить в FastAPI приложение ендпоинт, который будет принимать запросы с URL для парсинга от клиента, отправлять запрос парсеру (запущенному в отдельном контейнере) и возвращать ответ с результатом клиенту.
Зачем: Это позволит интегрировать функциональность парсера в ваше веб-приложение, предоставляя возможность пользователям запускать парсинг через API.
Полезные ссылки:
Документация FastAPI
Подзадача 3: Вызов парсера из FastAPI через очередь
Как это работает
Celery и Redis:

Celery — это асинхронная очередь задач, которая позволяет легко распределять и выполнять задачи в фоне. Redis используется как брокер сообщений, хранящий задачи, которые должны быть выполнены.
При получении HTTP-запроса, задача ставится в очередь Redis, и Celery-воркер обрабатывает её в фоне.

```python
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/personal_finance_web_lab')


async def parse_and_save(url, session, database):
    async with session.get(url) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')

        billionaires = soup.find_all("figcaption", class_="EXdHT")

        for billionaire in billionaires:
            name_tag = billionaire.find("h2", class_="jYzxi")
            balance_tag = billionaire.find("p", class_="ywx5e Q0w8z")

            if name_tag and balance_tag:
                name = name_tag.text.strip().split(" ", 1)[-1]
                balance_text = balance_tag.find("b", string=re.compile(r"Состояние:\s*"))

                if balance_text:
                    balance = balance_text.next_sibling.strip()
                else:
                    balance = balance_tag.find("b", string=re.compile(r"Доход:\с*")).next_sibling.strip()

                query = 'INSERT INTO finance (url, name, balance) VALUES (:url, :name, :balance)'
                values = {"url": url, "name": name, "balance": balance}
                await database.execute(query=query, values=values)


async def worker(urls, database):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(url, session, database) for url in urls]
        await asyncio.gather(*tasks)


async def main_start():
    urls = ["https://www.forbes.ru/milliardery/487053-10-bogatejsih-ludej-mira-2023-rejting-forbes",
            "https://www.forbes.ru/forbeslife/475277-samye-vysokooplacivaemye-tennisisty-mira-2022"]
    num_tasks = 1
    database = Database(DATABASE_URL)

    try:
        await database.connect()
        await database.execute('''
            CREATE TABLE IF NOT EXISTS finance (
                id SERIAL PRIMARY KEY,
                url TEXT,
                name TEXT,
                balance TEXT
            )
        ''')

        start_time = time.time()

        tasks = [asyncio.create_task(worker(urls[i::num_tasks], database)) for i in range(num_tasks)]
        await asyncio.gather(*tasks)

        await database.disconnect()
        end_time = time.time()
        return f"Parsed and saved data in {end_time - start_time} seconds"
    except Exception as e:
        return f"Unexpected error: {e}"


if __name__ == "__main__":
    asyncio.run(main_start())

```
```python
from celery import Celery
import asyncio
from parser import main_start

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def parse_urls():
    asyncio.run(main_start())

```
```python
broker_url = 'redis://redis:6379/0'
result_backend = 'redis://redis:6379/0'

```
```python
# main.py
from fastapi import FastAPI, BackgroundTasks
from celery_worker import parse_urls
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные окружения из .env

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/parse")
async def start_parsing(background_tasks: BackgroundTasks):
    task = parse_urls.delay()
    return {"task_id": task.id, "status": "started"}

```

```python
fastapi
aiohttp
beautifulsoup4
databases
asyncpg
celery
redis
uvicorn
python-dotenv

```
```yaml
services:
  database:
    image: postgres:latest
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: personal_finance_web_lab


  fastapi:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:80"
    depends_on:
      - database
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/personal_finance_web_lab

  parser:
    build:
      context: .
      dockerfile: DockerfileParser
    depends_on:
      - database
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/personal_finance_web_lab

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  celery_worker:
    build:
      context: .
      dockerfile: DockerfileParser
    command: celery -A celery_worker worker --loglevel=info
    depends_on:
      - database
      - redis
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/personal_finance_web_lab
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0

volumes:
  postgres_data:
```
```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .env

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

```

# Вывод

Научился поднимать dockerfile, поработал с очередью celery