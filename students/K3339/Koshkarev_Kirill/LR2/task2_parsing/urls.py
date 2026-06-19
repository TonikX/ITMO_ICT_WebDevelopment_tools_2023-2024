"""Список URL для параллельного парсинга и извлечение <title> из HTML.

Для извлечения заголовка используется стандартный html.parser (без сторонних
библиотек вроде BeautifulSoup).
"""
import gzip
import urllib.request
import zlib
from html.parser import HTMLParser

# Набор стабильных публичных страниц для демонстрации параллельного парсинга.
URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://docs.python.org/3/",
    "https://www.wikipedia.org",
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://en.wikipedia.org/wiki/Hackathon",
    "https://en.wikipedia.org/wiki/Concurrency_(computer_science)",
    "https://en.wikipedia.org/wiki/Thread_(computing)",
    "https://en.wikipedia.org/wiki/Process_(computing)",
    "https://en.wikipedia.org/wiki/Asynchronous_I/O",
    "https://www.iana.org/help/example-domains",
    "https://httpbin.org/html",
]


class _TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_title = False
        self.title_parts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)


def extract_title(html: str) -> str:
    """Возвращает текст из тега <title> или заглушку, если он не найден."""
    parser = _TitleParser()
    parser.feed(html)
    title = "".join(parser.title_parts).strip()
    # Убираем переносы строк и лишние пробелы внутри заголовка.
    title = " ".join(title.split())
    return title or "(без заголовка)"


def fetch_sync(url: str, timeout: int = 20) -> str:
    """Синхронная загрузка страницы для threading / multiprocessing / sequential.

    Корректно обрабатывает сжатие gzip/deflate (некоторые серверы, например
    python.org, отдают gzip даже без явного запроса).
    """
    req = urllib.request.Request(url, headers={"User-Agent": "LR2-parser/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        encoding = (resp.headers.get("Content-Encoding") or "").lower()
        if encoding == "gzip":
            raw = gzip.decompress(raw)
        elif encoding == "deflate":
            raw = zlib.decompress(raw)
        charset = resp.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")
