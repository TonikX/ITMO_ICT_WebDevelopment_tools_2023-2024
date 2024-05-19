from fastapi import APIRouter
from celery import current_app as celery_app

from celery_tasks.app import parse_title
from rest.celery_router.schemas import TaskIdResponse, TaskStatusResponse, ParsedDataResponse

router = APIRouter(prefix="/celery", tags=["celery"])


@router.post("/start_parsing")
async def start_parsing(url: str) -> TaskIdResponse:
    task = parse_title.delay(url)
    return TaskIdResponse.model_validate({"task_id": task.id})


@router.get("/check_parsing")
async def check_parsing(task_id: str) -> TaskStatusResponse:
    task = celery_app.AsyncResult(task_id)
    status = task.status

    return TaskStatusResponse.model_validate({"status": status})


@router.get("/get_parsing")
async def celery_get_csv(task_id: str) -> ParsedDataResponse:
    task = celery_app.AsyncResult(task_id)
    result = task.result

    data = result.get("data")

    return ParsedDataResponse.model_validate({"data": data})
