from bs4 import BeautifulSoup
from src.models import Page


def parse_and_save(url, html, sqlalchemy_worker):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string
    created_page = Page(url=url, title=title)

    return sqlalchemy_worker.create_object(created_page)
