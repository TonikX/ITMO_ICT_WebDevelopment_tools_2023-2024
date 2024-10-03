from fastapi import FastAPI, HTTPException
import requests
from parsing import parse_and_save, create_db
from celeryTask import parse_and_save as parse_and_save_celery

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db()

@app.get("/")
def hi():
    return "Hello"

@app.get("/celery")
def test(url: str):
    urls = [url]
    results = parse_and_save_celery.apply_async(args=[urls])
    return {"message": "Parsing started"}

@app.post("/parse")
def parse(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        parse_and_save(url)
        return {"message": "Parsing completed"}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
