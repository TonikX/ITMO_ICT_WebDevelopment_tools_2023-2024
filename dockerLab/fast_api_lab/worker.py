from celery import Celery
from sqlmodel import Session, create_engine, text
import os
import requests
from fastapi import HTTPException

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)


print(os.getenv("CELERY_BROKER_URL"), os.getenv("CELERY_RESULT_BACKEND"))
celery_app = Celery('fast_api_lab', broker=os.getenv("CELERY_BROKER_URL", 'redis://localhost:6379/0'),
                    backend=os.getenv("CELERY_RESULT_BACKEND", 'redis://localhost:6379/0'))

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'count-records-every-hour': {
            'task': 'count_records_task',
            'schedule': 3.0,  # каждый час
        },
    },
)


@celery_app.task(name="parse_urls_task")
def parse_urls_task(category: str):
    try:
        response = requests.post(f"http://async_lab:8080/parse/{category}")
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@celery_app.task(name="count_records_task")
def count_records_task():
    table_names = ["project", "task", "team", "user", "userprofile"]
    counts = {}

    with Session(engine) as session:
        for table_name in table_names:
            statement = text(f"SELECT COUNT(*) FROM {table_name}")
            result = session.execute(statement).one()
            counts[table_name] = result[0]

    return counts