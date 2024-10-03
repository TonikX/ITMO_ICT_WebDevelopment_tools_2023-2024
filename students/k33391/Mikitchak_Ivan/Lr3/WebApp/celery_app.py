from celery import Celery
from fastapi import APIRouter, HTTPException
import requests
from dotenv import load_dotenv
import os

load_dotenv()
broker_url = os.getenv("BROKER_URL")
backend_url = os.getenv("BACKEND_URL")
parser_url = os.getenv("PARSER_URL")
app = Celery("my_app", broker=broker_url, backend=backend_url)

@app.task
def parse_user() -> dict:
    with requests.Session() as session:
        try:
            response = session.get(url=parser_url)
        except Exception:
            raise HTTPException(status_code=500, detail="An error occured while fetching data.")
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Request failed with status code {response.status_code}.")
        
        user_data = response.json()
        return user_data
