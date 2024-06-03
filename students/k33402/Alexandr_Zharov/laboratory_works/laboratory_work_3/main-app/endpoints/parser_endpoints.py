import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.parser_models import ArticleResponse, UrlRequest

parser_router = APIRouter()

parsing_service_url = os.getenv("PARSING_SERVICE_URL")

@parser_router.post("/parser/", response_model=ArticleResponse)
def parse_url(url_request: UrlRequest):
    try:
        response = requests.post(f'{parsing_service_url}/parse', json={"url": url_request.url})
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error while contacting the parsing service: {e}")

    data = response.json()
    return data
