from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import config
import requests

from connection import DataBaseConnection
from bs4 import BeautifulSoup
from datetime import date, timedelta
from sqlalchemy.orm import sessionmaker
from celery import Celery

celery_app = Celery(
    "web_parser",
    result_backend=f"redis://redis:6379/0",
    broker="redis://redis:6379",
)

app = FastAPI()

class ParseRequest(BaseModel):
    url: str

@app.post("/parse/")
async def parse(request: ParseRequest):
    try:
        parse_and_save.delay(request.url)
        return {"message": f"Tasks were successfully saved!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@celery_app.task
def parse_and_save(url):
    try:
        engine = DataBaseConnection.connect_to_database()
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tasks = soup.find_all(config.HTML_TAG, class_=config.HTML_CLASS)
        task = tasks[0].text.strip().replace('\xa0', ' ')

        with session_local() as session:
            task_data = {
                'title': task,
                'description': '',
                'deadline': str(date.today() + timedelta(7)),
                'created_date': str(date.today()),
                'priority': 'high',
                'status': 'to_do',
                'category_id': 1,
                'user_id': 1
            }
            session.execute(DataBaseConnection.INSERT_SQL, task_data)
            session.commit()
    except Exception as e:
        print(f"Error in parse_and_save: {e}")
