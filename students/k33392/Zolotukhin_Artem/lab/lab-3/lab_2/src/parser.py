from .base import WebParserBase

class WebParser(WebParserBase):
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

