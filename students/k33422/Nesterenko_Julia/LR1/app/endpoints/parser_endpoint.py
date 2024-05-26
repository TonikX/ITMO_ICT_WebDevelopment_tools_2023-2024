from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict
import requests

from app.connection import *
from app.auth import AuthHandler

from app.celery_tasks import parse_celery

import os
from dotenv import load_dotenv


load_dotenv()
parser_url = os.getenv('PARSER_URL')


parse_router = APIRouter()
auth_handler = AuthHandler()


# basic parser call
@parse_router.post("/parse", tags=['Parser'], 
                   description='One of: "planes", "cruises", "trains", "airbnb", "hotels", "hostels"')
def parse_data(key: str):
    headers = {'accept': 'application/json'}
    data = {"key": key}
    response = requests.post(parser_url, headers=headers, params=data)
    return {"status": response.status_code, "response_msg": response.json()['message']}


# async parser call
@parse_router.post("/parse_async", tags=['Parser'], 
                   description='One of: "planes", "cruises", "trains", "airbnb", "hotels", "hostels"')
async def parse_data_async(key: str):
    result = parse_celery.delay(key)
    return {"message": "Parsing started", "task_id": result.id, "status": result.status}