from celery import Celery
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
import requests
import chardet
from bs4 import BeautifulSoup
from celery.result import AsyncResult
from datetime import datetime, timedelta, date
from models import Task, Category
from db import get_session
from celery_app import celery_app
from parsing import parse_and_save
from schemas import URLRequest

app = FastAPI()


@app.post("/celery-task")
async def celery_task_endpoint(request: URLRequest):
    try:
        print (request.url)
        task = celery_app.send_task('celery_app.parse_url_task', args=[str(request.url)])
        return {"task_id": task.id, "status": "Task has been submitted"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/celery-task-status/{task_id}")
async def get_celery_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == 'FAILURE':
        return {"task_id": task_id, "status": task_result.state, "error": str(task_result.result)}
    return {"task_id": task_id, "status": task_result.state, "result": task_result.result}



@app.post("/parse")
def parse(url: str, db: Session = Depends(get_session)):
    return parse_and_save(db=db, url=url)

