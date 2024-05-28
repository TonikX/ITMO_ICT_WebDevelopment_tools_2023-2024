from celery import Celery # type: ignore
from typing import Optional, TypedDict # type: ignore
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore

celery_app = Celery(
    'url_parser',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

class TripDTO(TypedDict):
    departure: Optional[str] = "Home"
    destination: str

@celery_app.task
def parse_url(url: str) -> Optional[TripDTO]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    destination = soup.title.string
    if not destination:
        return
    return {
        "destination": destination
    }

