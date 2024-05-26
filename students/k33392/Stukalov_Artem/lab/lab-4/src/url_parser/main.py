from celery import Celery
from typing import Optional, TypedDict
from abc import ABC
import httpx
from bs4 import BeautifulSoup, Tag, NavigableString


app = Celery(
    "url_parser",
    result_backend=f"redis://redis:6379/0",
    broker="redis://redis:6379",
)


class BookDTO(TypedDict):
    title: str
    author: str


class WebParser(ABC):
    log: bool

    def __init__(self) -> None:
        super().__init__()

    def _fetch_html_data(self, url: str) -> Optional[str]:
        with httpx.Client() as client:
            response = client.get(url)

        if response.status_code != 200:
            return
        return response.text

    def _check_if_tag(self, value: Tag | NavigableString | None) -> Optional[Tag]:
        if value is None or isinstance(value, NavigableString):
            return

        return value

    def _find_book_title(self, soup: BeautifulSoup) -> Optional[str]:
        tag = self._check_if_tag(soup.find(class_="book-page__title"))
        if tag is None:
            return

        return (tag.string or "").strip()

    def _find_book_author(self, soup: BeautifulSoup) -> Optional[str]:
        tag = self._check_if_tag(soup.find(class_="book-page__author"))
        if tag is None:
            return

        return (tag.string or "").strip()

    def _parse_content(self, content: str) -> Optional[BookDTO]:
        soup = BeautifulSoup(content, features="lxml")
        title = self._find_book_title(soup)
        author = self._find_book_author(soup)
        if not title or not author:
            return

        return {
            "title": title,
            "author": author,
        }

    def parse_url(self, url: str) -> BookDTO:
        content = self._fetch_html_data(url)
        if not content:
            raise Exception

        dto = self._parse_content(content)
        if not dto:
            raise Exception

        return dto


parser = WebParser()


@app.task
def parse_book(url: str):
    res = parser.parse_url(url)
    return {"res": res}
