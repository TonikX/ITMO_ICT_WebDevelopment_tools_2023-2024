from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
import psycopg2
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from celery.result import AsyncResult
import requests
from .celery_app import celery_app

app = FastAPI()

class URLItem(BaseModel):
    url: str

def parse_and_save(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').get_text()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {e}")

    try:
        conn = psycopg2.connect(dbname="web", user="postgres", password="serqet", host="db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO titles (url, title) VALUES (%s, %s)", (url, title))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return {"url": url, "title": title}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/parse")
def parse(url_item: URLItem, background_tasks: BackgroundTasks):
    task = celery_app.send_task("app.celery_app.parse_url", args=[url_item.url])
    return {"task_id": task.id}

@app.get("/result/{task_id}")
def get_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == "PENDING":
        return {"status": "PENDING"}
    elif task_result.state != "FAILURE":
        return {"status": task_result.state, "result": task_result.result}
    else:
        return {"status": task_result.state, "result": str(task_result.info)}