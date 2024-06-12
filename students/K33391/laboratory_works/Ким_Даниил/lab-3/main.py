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
