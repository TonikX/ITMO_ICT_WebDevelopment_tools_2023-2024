from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from celery.result import AsyncResult

from .parser_service import parse_and_save_books
from .celery_tasks import celery_app, parse_url_task

logger = logging.getLogger(__name__)

class InputUrl(BaseModel):
    url: str


app = FastAPI(
    title="Book Parser API",
    description="API для парсинга книг автора с LiveLib",
    version="1.0.0",
)

@app.post("/parse")
async def parse_author_books(data: InputUrl):
    try:
        books_parsed = await parse_and_save_books(data.url)

        return {
            "status": "success",
            "author_url": data.url,
            "books_parsed": books_parsed,
            "message": f"Successfully saved {books_parsed} new books"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Parsing error: {str(e)}"
        )

@app.post("/parse-async")
async def start_parsing(data: InputUrl):
    try:
        logger.info(f"Starting parsing task for URL: {data.url}")
        task = parse_url_task.delay(data.url)
        logger.info(f"Task created with id: {task.id}")

        return {
            "status": "processing",
            "task_id": task.id,
            "message": "Parsing task started successfully",
        }
    except Exception as e:
        logger.error(f"Failed to start task: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start parsing task: {str(e)}"
        )

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    try:
        task_result = AsyncResult(task_id, app=celery_app)

        response = {
            "task_id": task_id,
            "status": task_result.status,
        }

        if task_result.ready():
            if task_result.successful():
                response["result"] = task_result.result
                response["status"] = "completed"
            else:
                response["error"] = str(task_result.result)
                response["status"] = "failed"

        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting task status: {str(e)}"
        )