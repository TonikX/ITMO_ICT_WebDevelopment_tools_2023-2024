# Lab 3

Приложения были упакованы в Dockerfile, объединены в docker-compose, добавлена очередь celery с хранилищем redis.

Код был местами переработан для корректной работы контейнеризации.

Наблюдение за контейнерами было через Services внутри PyCharm.

Приложение app - результат ЛР1. 

Приложение сelery - результат работы ЛР2+ЛР3.

Ниже приведены переработанные и написанные файлы в рамках данной работы.

## Общий docker-compose.yml
```yaml
version: '3.9'

services:
  db:
    image: postgres:latest
    container_name: db
    ports:
      - "5432:5432"
    expose:
      - "5432:5432"
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:latest
    container_name: redis
    ports:
      - "6379:6379"
    restart: unless-stopped

  app:
    build: ./app
    container_name: app
    ports:
      - "3000:3000"
    env_file:
      - .env
    depends_on:
      - db
      - celery_app
    links:
      - "db:database"

  celery_app:
    build:
      context: ./celery
      dockerfile: Dockerfile
    container_name: celery_app
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - redis

  celery_worker:
    build:
      context: ./celery
    env_file:
      - .env
    container_name: celery_worker
    command: celery -A celery_worker worker -l info -E
    restart: unless-stopped
    depends_on:
      - redis
      - celery_app

volumes:
  postgres_data:
```

## App - code && screenshots
### Dockerfile
Описываем докерфайл для приложения по учету финансов из ЛР1. 
1. Из образа python:3.12 строим этот контейнер
2. Указываем рабочую директорию, где будут исполняться следующие команды
3. Копируем зависимости
4. Устанавливаем их
5. Копируем остальные файлы
6. Прокидываем наверх порт 8080
7. Выполняем команду "uvicorn main:app --host 0.0.0.0 --port 8080"
```dockerfile
FROM python:3.12
WORKDIR /app
COPY ../requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
EXPOSE 3000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
```

### main.py
```python
from fastapi import FastAPI
from router import customers, categories, operations, transactions
from db import *
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    get_session()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(customers.customerRouter)
app.include_router(categories.categoryRouter)
app.include_router(operations.operationRouter)
app.include_router(transactions.transactionRouter)
```

### Рабочие скриншоты
![3get_customers.png](src%2F3get_customers.png)
![3post_categories.png](src%2F3post_categories.png)
![3post_customers.png](src%2F3post_customers.png)

## Celery - code && screenshots
### Dockerfile
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### main.py
```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from tasks import parse
from celery_app import celery_app

app = FastAPI()


class URL(BaseModel):
    url: str


@app.post("/")
async def parse_url(item: URL, background_tasks: BackgroundTasks):
    background_tasks.add_task(parse, item.url)
    celery_app.send_task('tasks.parse', args=[item.url])
    return {"message": "started"}
    # redis-cli lrange queue 0 100


@app.get("/")
async def get():
    return {"message": "Hello world"}
```

### tasks.py
```python
import requests
from bs4 import BeautifulSoup
from connection import DBConn
from celery_app import celery_app


@celery_app.task
def parse(url):
    con = DBConn.connect_to_database()
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')  # создаем парсер
        articles = soup.find_all('article', class_='tm-articles-list__item')
        for article in articles:
            author = article.find('a', class_='tm-user-info__username').text
            datetime = article.find('a', class_='tm-article-datetime-published tm-article-datetime-published_link').text
            title = article.find('a', class_='tm-title__link').text
            with con.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                cursor.execute(DBConn.INSERT_SQL, (title, author, datetime))
        con.commit()
    except Exception as e:
        print("Ошибка:", e)
        con.rollback()
    con.close()
```

### celery_app.py
```python
import celery

celery_app = celery.Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    task_routes={"tasks.parse": "queue"},
)
```

### celery_worker.py
```python
from celery_app import celery_app
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    celery_app.broker_transport_options = {os.getenv("CELERY_REDIS_URL")}
    celery_app.start()
```

### Рабочие скриншоты
![3redis_get.png](src%2F3redis_get.png)
![3get_celery.png](src%2F3get_celery.png)