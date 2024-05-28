from fastapi import APIRouter
from fastapi.responses import Response
from http import HTTPStatus
from .models import ParseRequest
import aiohttp
from celery import Celery
from celery.result import AsyncResult

router = APIRouter(prefix="/parse")
app = Celery("parser")
app.autodiscover_tasks()

@router.post("")
async def parse(req: ParseRequest):
    async with aiohttp.ClientSession() as client:
        async with client.post("http://parser:8080/parse", json=dict(req)) as resp:
            return await resp.json()

@router.post("/celery/sync")
def parse_celery_sync(req: ParseRequest):
    result = app.send_task("tasks.parse", args=[req.parser])
    return result.get(timeout=10)

@router.post("/celery/async")
def parse_async(req: ParseRequest):
    task = app.send_task("tasks.parse", args=[req.parser])
    return task.as_list()

@router.get("/celery/task")
def get_task_result(task_id: str):
    result = AsyncResult(task_id, app=app)
    if not result.ready():
        return Response(HTTPStatus.ACCEPTED)
    return result.get()
