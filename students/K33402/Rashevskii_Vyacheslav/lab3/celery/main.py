from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from tasks import parse_and_save_threading
from celery_app import celery_app

# URLs = [
#     'https://github.com/TonikX/ITMO_ICT_WebDevelopment_tools_2023-2024/pulls?page=1&q=is%3Apr+is%3Aopen',
#     'https://github.com/TonikX/ITMO_ICT_WebDevelopment_tools_2023-2024/pulls?page=2&q=is%3Apr+is%3Aopen',
#     'https://github.com/TonikX/ITMO_ICT_WebDevelopment_tools_2023-2024/pulls?page=3&q=is%3Apr+is%3Aopen',
#     'https://github.com/TonikX/ITMO_ICT_WebDevelopment_2022-2023/pulls?page=1&q=is%3Apr+is%3Aopen',
#     'https://github.com/TonikX/ITMO_ICT_WebDevelopment_2022-2023/pulls?page=2&q=is%3Apr+is%3Aopen',
#     'https://github.com/TonikX/ITMO_ICT_WebDevelopment_2022-2023/pulls?page=3&q=is%3Apr+is%3Aopen',
# ]

app = FastAPI()


class URL(BaseModel):
    url: str


@app.post("/")
async def parse_url(item: URL, background_tasks: BackgroundTasks):
    background_tasks.add_task(parse_and_save_threading, item.url)
    celery_app.send_task('tasks.parse_and_save_threading', args=[item.url])
    return {"message": "started"}
    # https://github.com/TonikX/ITMO_ICT_WebDevelopment_tools_2023-2024/pulls?page=1&q=is%3Apr+is%3Aopen
    # redis-cli lrange main-queue 0 1000


@app.get("/")
async def get():
    print("get")
    return {"message": "got main page"}
