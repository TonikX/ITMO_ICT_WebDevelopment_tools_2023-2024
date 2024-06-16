from typing import Optional, TypedDict
from abc import ABC, abstractmethod
import httpx
from bs4 import BeautifulSoup, Tag, NavigableString
from sqlmodel import Session, select
from .db import engine
from .models import Book, BookModerationStatus


class BookDTO(TypedDict):
    title: str
    author: str


class WebParserBase(ABC):
    log: bool

    def __init__(self, log: bool) -> None:
        self.log = log
        super().__init__()

    def _fetch_html_data(self, url: str) -> Optional[str]:
        with httpx.Client() as client:
            response = client.get(url)

        if response.status_code != 200:
            if self.log:
                print(
                    f"Failed status code for url: {url} status: {response.status_code}"
                )
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
        soup = BeautifulSoup(content, 'html.parser')
        title = self._find_book_title(soup)
        author = self._find_book_author(soup)
        if not title or not author:
            return

        return {
            "title": title,
            "author": author,
        }

    def _save_db_sync(self, value: BookDTO) -> None:
        with Session(engine) as session:
            statement = select(Book).where(Book.title == value["title"])
            existing_book = session.exec(statement).first()
            if existing_book:
                if self.log:
                    print(f'Trying to save existing book with title: {value["title"]}')
                return

            book = Book(
                title=value["title"],
                author=value["author"],
                creator_id=1,
                moderation_status=BookModerationStatus.approved,
            )
            session.add(book)
            session.commit()

    @abstractmethod
    def parse_and_save(self, url: str) -> None: ...
