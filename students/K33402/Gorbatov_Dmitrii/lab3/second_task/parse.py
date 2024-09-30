from celery_app import celery_app
from connection import get_session, Site
import requests
from bs4 import BeautifulSoup

@celery_app.task(name="parse_and_save")
def parse_and_save(url):
    with get_session() as session:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title'
        new_article = Site(url=url, title=title, method="GET")
        session.add(new_article)
        session.commit()
