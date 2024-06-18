import requests
from bs4 import BeautifulSoup
from celery_main import celery_app
from schemas import Parse


@celery_app.task
def parse_and_save(url, session):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title"

    new_article = Parse(url=url, article_title=title)

    session.add(new_article)
    session.commit()
