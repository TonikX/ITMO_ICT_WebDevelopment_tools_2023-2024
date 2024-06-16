from src.base import WebParserBase
from src.config import URLS
import asyncio
from typing import List, Optional
import httpx


class WebParserAsync(WebParserBase):
    async def _fetch_html_data(self, url: str) -> Optional[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            if self.log:
                print(
                    f"Failed status code for url: {url} status: {response.status_code}"
                )
            return
        return response.text

    async def parse_and_save(self, url: str) -> None:
        if self.log:
            print(f"Start url: {url}")

        content = await self._fetch_html_data(url)
        if not content:
            if self.log:
                print(f"Failed fetch url: {url}")
            return

        dto = self._parse_content(content)
        if not dto:
            if self.log:
                print(f"Failed get dto url: {url}")
            return

        await self._save_db_async(dto)
        if self.log:
            print(f"Finish url: {url}")

    async def parse_many(self, urls: List[str]) -> None:
        tasks = [asyncio.create_task(self.parse_and_save(url)) for url in urls]
        await asyncio.gather(*tasks)


def start():
    asyncio.run(WebParserAsync(False).parse_many(URLS))


if __name__ == "__main__":
    start()
