# Лабораторная часть

Ниже представлен код с подробными комментариями и скрины рабочие.

Сервисы описаны, объединены в одну сеть и docker с помощью docker-compose.
## docker-compose.yml
```yaml
services:
  celery_app:
    build:
      context: ./celery
      dockerfile: Dockerfile
    container_name: celery_app
    restart: unless-stopped
    ports:
      - "8081:8081"
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
      - "8080:8080"
    env_file:
      - .env
    depends_on:
      - db
      - celery_app
    links:
      - "db:database"

  db:
    image: postgres:latest
    container_name: db
    env_file:
      - .env
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

volumes:
  postgres_data:
```

## app/...
В папке app находится весь код из ЛР1 и дописан Dockerfile
```dockerfile
FROM python:3.12

WORKDIR /app

COPY ../requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## celery/...
В папке celery находится подключение к redis, где хранятся сообщения, которые попадают туда через очередь celery, а также перенесена часть ЛР2.

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
```

## celery_app.py
Описана очередь с заданными ссылками и названием, а также указаны некоторые настройки таймзоны, очереди и serializer.
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
    timezone='UTC',
    enable_utc=True,
    task_routes={
        "tasks.parse_and_save_threading": "main-queue",
    },
)

```

## celery_worker.py
Загружаются переменные среды и запускается приложение с указанным URL.
```python
from celery_app import celery_app
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    redis_url = os.getenv("CELERY_REDIS_URL")
    celery_app.broker_transport_options = {redis_url}
    celery_app.start()

```

## tasks.py
Описана задача из ЛР2 и помечена декоратором.
```python
import requests
from bs4 import BeautifulSoup
from db import DBConn
from celery_app import celery_app


@celery_app.task
def parse_and_save_threading(url):
    db_conn = DBConn.connect_to_database()
    try:  # пробуем, поскольку может упасть исключение
        page = requests.get(url)  # получаем страницу
        soup = BeautifulSoup(page.text, 'html.parser')  # создаем парсер
        books = soup.find_all('div', class_='product-card')  # находим все блоки книг по классу
        for book in books:  # проходимся в цикле по всем книгам
            title = book.attrs['data-product-name']  # получаем название книги
            price = book.attrs['data-product-price-discounted']  # получаем цену книги

            with db_conn.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                cursor.execute(DBConn.INSERT_SQL, (title, price))  # выполняем ранее написанную команду и передаем в нее аргументы

        db_conn.commit()  # подтверждаем изменения
    except Exception as e:  # при получении исключения
        print("Ошибка:", e)  # выводим ошибку
        db_conn.rollback()  # откатываем изменения
    finally:
        db_conn.commit()
        db_conn.close()
```

## main.py
Определение приложение я 2-ух эндпоинтов.
```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from tasks import parse_and_save_threading
from celery_app import celery_app

app = FastAPI()


class URL(BaseModel):
    url: str


@app.post("/")
async def parse_url(item: URL, background_tasks: BackgroundTasks):
    background_tasks.add_task(parse_and_save_threading, item.url)
    celery_app.send_task('tasks.parse_and_save_threading', args=[item.url])
    return {"message": "started"}
    # redis-cli lrange main-queue 0 1000


@app.get("/")
async def get():
    print("get")
    return {"message": "got main page"}
```

