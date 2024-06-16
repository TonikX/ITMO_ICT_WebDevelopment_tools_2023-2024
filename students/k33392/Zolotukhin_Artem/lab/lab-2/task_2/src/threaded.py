from src.base import WebParserBase
from src.config import URLS
import threading
from typing import List


class WebParserThreaded(WebParserBase):
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
        threads: List[threading.Thread] = []

        for url in urls:
            thread = threading.Thread(
                target=self.parse_and_save,
                args=(url,),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


def start():
    WebParserThreaded(False).parse_many(URLS)


if __name__ == "__main__":
    start()
