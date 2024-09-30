#Лабораторная работа - 3
###Задание
Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с базой данных и вызывать парсер через API и очередь.

###Реализация парсера

```py 
from fastapi import APIRouter, Depends
from connection import get_session
from models import Site
import aiohttp
from bs4 import BeautifulSoup

router = APIRouter()

async def parse_and_save_async(url: str, session) -> str:
    async with aiohttp.ClientSession() as aio_session:
        response = await fetch_page(aio_session, url)
        soup = BeautifulSoup(response, 'html.parser')
        title_tag = soup.title
        if title_tag:
            title = title_tag.string
        else:
            title = ""  # or some default value
        site = Site(url=url, title=title, method='async')
        session.add(site)
        session.commit()
        session.refresh(site)
        return title  # Return the title value
async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, ssl=False) as response:
        return await response.text()

@router.post("/parse")
async def parse(url: str, session=Depends(get_session)):
        data = await parse_and_save_async(url, session)
        return {"data": data}
```

###docker-compose

```py 
services:
  db:
    image: postgres
    container_name: db
    restart: always
    environment:
      - POSTGRES_PASSWORD=123
      - POSTGRES_USER=postgres
      - POSTGRES_DB=lab3
      - POSTGRES_PORT=5432
    volumes:
      - db-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - my_network

  app:
    container_name: app
    build:
      context: .
    env_file: .env
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    restart: always
    networks:
      - my_network

  celery_task:
    container_name: celery_task
    build:
      context: ./second_task
    env_file: .env
    depends_on:
      - db
      - redis
    ports:
      - "8001:8001"
    command: uvicorn main:app --host 0.0.0.0 --port 8001
    restart: always
    networks:
      - my_network
    dns:
      - 8.8.8.8
      - 8.8.4.4

  celery:
    build:
      context: ./second_task
    container_name: celery
    command: celery -A parse worker --loglevel=info
    restart: always
    depends_on:
      - redis
      - db
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    networks:
      - my_network

  redis:
    image: redis
    ports:
      - "6379:6379"
    networks:
      - my_network

volumes:
  db-data:
networks:
  my_network:
```

###Dockerfile
```py 
FROM python:3.9-slim

WORKDIR /lab3

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]
```

###Реализация celery

celery_app.py

```py 
from celery import Celery

celery_app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")


celery_app.autodiscover_tasks(['parse'])
```

parse.py

```py 
from celery_app import celery_app
from connection import get_session, Site
import requests
from bs4 import BeautifulSoup

@celery_app.task(name="parse_and_save")
def parse_and_save(url):
    with get_session() as session:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title'
        new_article = Site(url=url, title=title, method="GET")
        session.add(new_article)
        session.commit()
```

main.py

```py 
from fastapi import FastAPI, BackgroundTasks
from connection import init_db
from celery_app import celery_app
from sqlmodel import Session, select
from connection import engine, Site

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/parse")
def parse(url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(celery_app.send_task, "parse_and_save", args=(url,))
    return {"message": "Parsing task triggered"}

@app.get("/results")
def get_results():
    with Session(engine) as session:
        results = session.exec(select(Site)).all()
    return results
```


