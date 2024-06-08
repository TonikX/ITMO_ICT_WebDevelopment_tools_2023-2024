from celery_config import celery_app
from sqlalchemy.orm import Session
from connection import SessionLocal
from parser import parse_and_save

@celery_app.task
def parse_url_task(url: str):
    db: Session = SessionLocal()
    try:
        parse_and_save(url, db)
    finally:
        db.close()
