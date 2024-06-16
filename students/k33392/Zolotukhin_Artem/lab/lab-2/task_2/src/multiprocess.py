from src.base import WebParserBase
from src.config import URLS
import multiprocessing
from typing import List


class WebParserMultiprocess(WebParserBase):
    def parse_and_save(self, url: str) -> None:
        if self.log:
            print(f"Start url: {url}")

        content = self._fetch_html_data(url)
        if not content:
            if self.log:
                print(f"Failed fetch url: {url}")
            return

        dto = self._parse_content(content)
        if not dto:
            if self.log:
                print(f"Failed get dto url: {url}")
            return

        self._save_db_sync(dto)
        if self.log:
            print(f"Finish url: {url}")

    def parse_many(self, urls: List[str]) -> None:
        with multiprocessing.Pool(processes=len(urls)) as pool:
            pool.map(self.parse_and_save, urls)


def start():
    WebParserMultiprocess(False).parse_many(URLS)


if __name__ == "__main__":
    start()
