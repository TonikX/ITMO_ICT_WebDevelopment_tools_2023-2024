"""Общая логика парсинга страницы и сохранения результата в БД.

Используется и сервисом-парсером (parser/main.py), и Celery-задачей
(worker/celery_app.py): оба загружают страницу, извлекают <title> и пишут
запись в таблицу parsed_pages.
"""
from html.parser import HTMLParser

import httpx

from app.database import AsyncSessionLocal
from app.models import ParsedPage


class _TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.parts.append(data)


def extract_title(html: str) -> str:
    parser = _TitleParser()
    parser.feed(html)
    title = " ".join("".join(parser.parts).split())
    return title or "(без заголовка)"


async def fetch_html_async(url: str, timeout: float = 20.0) -> str:
    """Асинхронно загружает HTML по URL (httpx сам распаковывает gzip/deflate)."""
    headers = {"User-Agent": "LR3-parser/1.0"}
    async with httpx.AsyncClient(follow_redirects=True, headers=headers, timeout=timeout) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text


async def parse_and_save_async(url: str, source: str) -> dict:
    """Асинхронно грузит страницу, извлекает заголовок и НЕблокирующе пишет в БД."""
    html = await fetch_html_async(url)
    title = extract_title(html)

    async with AsyncSessionLocal() as session:
        page = ParsedPage(url=url, title=title, source=source)
        session.add(page)
        await session.commit()
        await session.refresh(page)
        return {"id": page.id, "url": url, "title": title, "source": source}
