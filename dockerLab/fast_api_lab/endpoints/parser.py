from fastapi import APIRouter, HTTPException, BackgroundTasks
import requests
import asyncio
from worker import celery_app

parser_router = APIRouter()


@parser_router.post("/parse/{category}")
async def parse(category: str):
    try:
        response = requests.post(f"http://async_lab:8080/parse/{category}")
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@parser_router.post("/celery-parse/{category}")
async def parse(category: str, background_tasks: BackgroundTasks):
    print("parsing")
    try:
        # Постановка задачи в очередь Celery

        task = celery_app.send_task('parse_urls_task', args=[category])

        # Добавление фоновой задачи для проверки статуса задачи
        background_tasks.add_task(check_task_status, task.id)

        return {"task_id": task.id, "status": "Task has been started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def check_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)
    while not result.ready():
        await asyncio.sleep(1)
    return result.result
