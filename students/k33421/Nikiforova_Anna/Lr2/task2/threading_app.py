from base import AbstractSyncScrapper, urls
from database import Session
from models import Coctail, Ingredient, Property
import threading
import time


class URLProcessingThread(threading.Thread):
    def __init__(self, url, scrapper_instance):
        super().__init__()
        self.url = url
        self.scrapper_instance = scrapper_instance

    def run(self):
        html = self.scrapper_instance.get_html(self.url)
        raw_data = self.scrapper_instance.parse_html(html)
        self.scrapper_instance.save_data(raw_data)


class ThreadingScrapper(AbstractSyncScrapper):
    def __str__(self) -> str:
        return "ThreadingScrapper"
    
    def parse_and_save(self, urls: list[str]) -> float:
        start_time = time.time()
        threads = []

        for url in urls:
            thread = URLProcessingThread(url, self)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        end_time = time.time()
        execution_time = end_time - start_time
        return execution_time


if __name__ == '__main__':
    print("Time:", ThreadingScrapper().parse_and_save(urls))
