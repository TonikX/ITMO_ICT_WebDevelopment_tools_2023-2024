import datetime

import requests
from bs4 import BeautifulSoup
from celery import Celery
from sqlmodel import Session

from config import settings
from db.connection import engine
from db.models import Hackathon, Task

app = Celery(
    "celery_app",
    result_backend=f"redis://{settings.redis_host}:{settings.redis_port}/0",
    broker=f"pyamqp://guest@{settings.rabbitmq_host}:{settings.rabbitmq_port}//",
)


@app.task
def parse_hackathon(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    hack_name = soup.find("h1").text
    paragraphs = list(map(lambda x: x.text, soup.find_all('p')))
    hack_case = '\n'.join(paragraphs)
    case_title = paragraphs[0]

    with Session(engine) as session:
        hackathon = Hackathon(
            name=hack_name,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        session.add(hackathon)
        session.commit()
        session.refresh(hackathon)

        task = Task(
            title=case_title,
            description=hack_case,
            requirements="Be cool",
            evaluation_criteria="Accuracy",
            hackathon_id=hackathon.id
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        print(hackathon.name)

        return {"hackathon": hackathon.model_dump(), "task": task.model_dump()}
