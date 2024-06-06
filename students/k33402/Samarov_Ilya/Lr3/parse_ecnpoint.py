from fastapi import APIRouter, Depends, BackgroundTasks
from database import get_session
import requests
from models import Try
from bs4 import BeautifulSoup
from celery_app import celery_app


parse_router = APIRouter()


@celery_app.task
def parse_and_save(url, session):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No title'
    try_obj = Try(url=url, title=title)
    session.add(try_obj)
    session.commit()
    session.refresh(try_obj)


@parse_router.post("/parse")
def travel_create(url: str, background_tasks: BackgroundTasks, session=Depends(get_session)):
    background_tasks.add_task(parse_and_save, url, session)
    return {"message": "Parse started."}
