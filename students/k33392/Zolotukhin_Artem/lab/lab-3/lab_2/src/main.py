from fastapi import FastAPI, BackgroundTasks
from celery import Celery
from .parser import WebParser

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    task_routes={
        "parse.parse_and_save": "main-queue",
    },
)

app = FastAPI()

@celery_app.task
def celery_parse(url):
    WebParser(False).parse_and_save(url)


@app.post("/parse/")
async def parse(url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(celery_parse, url)
    return {"message": "Parse started."}
