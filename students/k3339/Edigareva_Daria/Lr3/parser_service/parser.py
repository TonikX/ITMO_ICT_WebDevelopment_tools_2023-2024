from __future__ import annotations

from typing import Tuple

import httpx
from bs4 import BeautifulSoup


async def fetch_html_and_title(url: str, timeout: float = 10.0) -> Tuple[str, str]:
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        html_text: str = resp.text

    soup = BeautifulSoup(html_text, "lxml")
    title_tag = soup.find("title")
    title = title_tag.text.strip() if title_tag else ""
    return title, html_text