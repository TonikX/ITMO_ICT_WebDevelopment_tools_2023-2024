from base import AbstractSyncScrapper, urls
from database import Session
from models import Coctail, Ingredient, Property
import multiprocessing
import httpx
import time
import os

# os.cpu_count()  # techniacally, on my machine I have 8 - this is the max number of processes


class MultiprocessingScrapper(AbstractSyncScrapper):
    def __str__(self) -> str:
        return "MultiprocessingScrapper"

    def process_url(self, url):
        html = self.get_html(url)
        raw_data = self.parse_html(html)
        self.save_data(raw_data)

    def parse_and_save(self, urls: list[str]) -> float:
        start_time = time.time()
        with multiprocessing.Pool() as pool:
            pool.map(self.process_url, urls)

        end_time = time.time()
        execution_time = end_time - start_time
        return execution_time


if __name__ == '__main__':
    print("Time:", MultiprocessingScrapper().parse_and_save(urls))
