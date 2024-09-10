from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from tasks import parse
from celery_app import celery_app

app = FastAPI()


class URL(BaseModel):
    url: str


@app.post("/")
async def parse_url(item: URL, background_tasks: BackgroundTasks):
    background_tasks.add_task(parse, item.url)
    celery_app.send_task('tasks.parse', args=[item.url])
    return {"message": "started"}
    # redis-cli lrange queue 0 100


@app.get("/")
async def get():
    return {"message": "Hello world"}
