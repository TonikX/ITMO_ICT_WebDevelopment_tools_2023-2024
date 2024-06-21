## Подготовка

Для реализации лабораторной будем использовать asyncio, т.к. она лучше всего показала себя при работе с парсингом веб-страниц. Для этого, реализуем сам парсер.

### parser.py

```python
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from sqlmodel import Session
from database.models import WebPage
from database.database import create_db_and_tables, engine

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
            return {"url": url, "title": title}
    except Exception as e:
        print(f"Ошибка парсинга {url}: {e}")
        return {"url": url, "title": None, "error": str(e)}

async def main(urls):
    create_db_and_tables()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(parse_and_save(url, session))
        results = await asyncio.gather(*tasks)
        return results
```

Реализуем celery, которое будет вызывать parser

### parser.py

```python
from celery import Celery
import asyncio
from app.parser import main as async_parser

celery_app = Celery(__name__, broker="redis://redis:6379/0", backend="redis://redis:6379/0")

@celery_app.task(name="app.tasks.parse_urls_async")
def parse_urls_async(urls: list[str]):
    result = asyncio.run(async_parser(urls))
    return result
```

Реализуем сервер и 3 метода для работы с парсингом.

### main.py

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from app.tasks import parse_urls_async, celery_app
from database.database import create_db_and_tables, get_session
from database.models import WebPage

app = FastAPI()

class ParseRequest(BaseModel):
    urls: list[str]

class ParseResponse(BaseModel):
    id: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/syncParse")
def sync_parse(request: ParseRequest):
    task = parse_urls_async.delay(request.urls)
    task.wait()  # Ожидание завершения задачи
    if task.state == 'SUCCESS':
        return {"status": task.state, "result": task.result}
    else:
        return {"status": "FAILURE", "result": str(task.info)}

@app.post("/asyncParse", response_model=ParseResponse)
def async_parse(request: ParseRequest):
    task = parse_urls_async.delay(request.urls)
    return {"id": task.id}

@app.get("/getParseData/{task_id}")
def get_parse_data(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        return {"status": "PENDING"}
    elif task_result.state == 'SUCCESS':
        return {"status": task_result.state, "result": task_result.result}
    else:
        return {"status": "FAILURE", "result": str(task_result.info)}
```

И вспомогательные файлы

### config.py

```python
class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/mydatabase"
    CELERY_BROKER_URL = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND = "redis://redis:6379/0"
```

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

### models.py

```python
from app.tasks import celery_app

if __name__ == "__main__":
    celery_app.start()

```

### celery_worker.py

```python
from app.tasks import celery_app

if __name__ == "__main__":
    celery_app.start()
```

## Итог

В результате получаем fastapi приложение которое позволяет парсить заголовки веб-страниц
