import requests
from fastapi import APIRouter, HTTPException

PARSER_SERVICE_URL = "http://parser:8000/celery-task"

router = APIRouter()

@router.post("/parse-url")
def parse_url(url: str):
    try:
        response = requests.post(PARSER_SERVICE_URL, json={"url": url})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=505, detail=str(e))

@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    response = requests.get(f"http://parser:8000/celery-task-status/{task_id}")
    return response.json()