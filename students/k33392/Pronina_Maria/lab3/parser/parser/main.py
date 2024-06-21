from typing import List
from models import User, UserProject
from sqlalchemy.future import select
from fastapi import FastAPI, HTTPException
from celery_config import celery_app


app = FastAPI()


@app.post("/parse")
async def parse(usernames: List[str]):
    try:
        task = celery_app.send_task('celery_config.parsing_task', args=[usernames])
        return {"task_id": task.id, "status": "Task has been submitted"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
