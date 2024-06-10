import requests
from fastapi import APIRouter

parser_url = "http://web_parser:8081/parse"

router = APIRouter()

@router.get("", response_model=dict)
def parse(url: str):
    response = requests.post(parser_url, json={'url': url})
    return response.json()
