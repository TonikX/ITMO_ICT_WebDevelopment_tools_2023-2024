from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from celery_backend.tasks import parse_task

app = FastAPI()


class TaskDto(BaseModel):
    task_id: str


class ResultDto(BaseModel):
    title: str

@app.post("/tasks")
async def place_task(url: str) -> TaskDto:
    task = parse_task.delay(url)
    return TaskDto(task_id=task.id)


@app.get("/tasks/{task_id}")
async def get_task_result(task_id: str):
    result = AsyncResult(task_id)
    try:
        r = result.get()
        return ResultDto(title=r["title"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

