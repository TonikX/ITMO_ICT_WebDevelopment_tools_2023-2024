import requests
from celery import shared_task
from fastapi import APIRouter, HTTPException

parser_url = "http://parser:8081/parse"

router = APIRouter(prefix="/parser", tags=["Parser"])


@router.get("", response_model=dict)
def parse(url: str):
    return requests.post(parser_url, params={'url': url}).json()
