import os

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter
from celery.result import AsyncResult
from broker.celery_app import celery_app

# Загрузка переменных окружения из .env файла
load_dotenv()

PARSER_URL = os.getenv("PARSER_URL")


parser_router = APIRouter()


@parser_router.post('/parse', status_code=201, description='Parse books')
def parse(url: str):
    with httpx.Client() as client:
        params = {'url': url}
        response = client.post(PARSER_URL + "/api/parser/parse", params=params)
        return response.json()

@parser_router.post("/celery-task")
async def celery_task_endpoint(url: str):
    task = celery_app.send_task('broker.celery_app.parse_books', args=[url])
    return {"task_id": task.id, "status": "Task has been submitted"}


@parser_router.get("/celery-task-status/{task_id}")
async def get_celery_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == 'FAILURE':
        return {"task_id": task_id, "status": task_result.state, "error": str(task_result.result)}
    return {"task_id": task_id, "status": task_result.state, "result": task_result.result}