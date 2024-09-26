from fastapi import FastAPI, BackgroundTasks
from connection import init_db
from celery_app import celery_app
from sqlmodel import Session, select
from connection import engine, Site

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/parse")
def parse(url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(celery_app.send_task, "parse_and_save", args=(url,))
    return {"message": "Parsing task triggered"}

@app.get("/results")
def get_results():
    with Session(engine) as session:
        results = session.exec(select(Site)).all()
    return results
