from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from app.tasks import parse_urls_async, celery_app
from database.database import create_db_and_tables, get_session
from database.models import WebPage

app = FastAPI()

class ParseRequest(BaseModel):
    urls: list[str]

class ParseResponse(BaseModel):
    id: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/syncParse")
def sync_parse(request: ParseRequest):
    task = parse_urls_async.delay(request.urls)
    task.wait()  # Ожидание завершения задачи
    if task.state == 'SUCCESS':
        return {"status": task.state, "result": task.result}
    else:
        return {"status": "FAILURE", "result": str(task.info)}

@app.post("/asyncParse", response_model=ParseResponse)
def async_parse(request: ParseRequest):
    task = parse_urls_async.delay(request.urls)
    return {"id": task.id}

@app.get("/getParseData/{task_id}")
def get_parse_data(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        return {"status": "PENDING"}
    elif task_result.state == 'SUCCESS':
        return {"status": task_result.state, "result": task_result.result}
    else:
        return {"status": "FAILURE", "result": str(task_result.info)}
