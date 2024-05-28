from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from celery_backend.tasks import long_running_task

app = FastAPI()


class TaskDto(BaseModel):
    task_id: str


@app.post("/tasks")
async def place_task(url: str) -> TaskDto:
    task = long_running_task.delay(url)
    return TaskDto(task_id=task.id)


@app.get("/tasks/{task_id}")
async def get_task_result(task_id: str):
    result = AsyncResult(task_id)
    try:
        return result.get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

