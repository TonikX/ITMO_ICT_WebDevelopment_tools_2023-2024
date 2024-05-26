from base import AbstractSyncScrapper, urls
from database import Session
from models import Coctail, Ingredient, Property
import httpx
import time


class SimpleScrapper(AbstractSyncScrapper):
    def __str__(self) -> str:
        return "SimpleScrapper"

    def parse_and_save(self, urls: list[str]) -> float:
        start_time = time.time()
        for url in urls:
            html = self.get_html(url)
            raw_data = self.parse_html(html)
            self.save_data(raw_data)
        end_time = time.time()
        execution_time = end_time - start_time
        return execution_time


if __name__ == '__main__':
    print("Time:", SimpleScrapper().parse_and_save(urls))
