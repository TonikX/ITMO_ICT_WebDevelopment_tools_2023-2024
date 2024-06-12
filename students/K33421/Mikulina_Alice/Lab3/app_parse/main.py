from fastapi import FastAPI, HTTPException
import requests
import asyncio
import uvicorn
from pydantic import BaseModel
from parsers.parser import parse_and_save_task
from celery_conf import app as celery_app
from celery.result import AsyncResult

# urls = [
#     'https://mybooklist.ru/list/1029',
#     'https://mybooklist.ru/list/483',
#     'https://mybooklist.ru/list/1204',
#     'https://mybooklist.ru/list/480'
# ]


class ParseModel(BaseModel):
    url: str
    user_id: int


app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.post("/parse")
async def parse(request: ParseModel):
    try:
        task = parse_and_save_task.delay(request.url, request.user_id)
        return {
            "task_id": task.id,
            "status": task.state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/parse/status")
async def parse_state(task_id: str):
    task_res = AsyncResult(task_id, app=celery_app)
    if task_res.ready():
        return {
            "status": task_res.state,
            "result": task_res.result
        }
    return {"status": task_res.state}


@app.get("/tasks")
async def get_tasks():
    inspect = celery_app.control.inspect()
    return {
        "registered": inspect.registered(),
        "active": inspect.active(),
        "scheduled": inspect.scheduled(),
        "reserved": inspect.reserved()
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
