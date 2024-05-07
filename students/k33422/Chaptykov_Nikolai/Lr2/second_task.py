from urllib.parse import unquote
from os import path, makedirs, cpu_count
from pygsheets.exceptions import InvalidArgumentValue, IncorrectCellLabel
from typing import Tuple, List
import time
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from multiprocessing import Process
import concurrent.futures
import asyncio
from threading import Thread
from typing import Tuple
import sys
import json


CPU_COUNT = cpu_count()
NUMBER_OF_WORKERS = CPU_COUNT if CPU_COUNT < 4 else CPU_COUNT - 1

"""
Базовая ссылка выглядит так:
url = 'https://joyreactor.cc/tag/котэ/7491'


Парсим новые посты:

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')
posts = soup.findAll('a', class_='prettyPhotoLink')
videos = soup.findAll('video')


print(posts[0].find("img").get("src"))
-> https://img2.joyreactor.cc/pics/post/котэ-999.jpeg

print(videos[0].find("source").get("src"))
-> https://img2.joyreactor.cc/pics/post/webm/гифки-живность-котэ-gif-8417001.webm


Создаем списки всех ссылок на картинки и видео со страницы:

vid_links = [tag.find("source").get("src") for tag in videos]
img_links = [tag.find("img").get("src") for tag in posts]
"""


class BackendHandler:
    def __init__(self):
        self.url = "http://127.0.0.1:8000/"
        self.session = requests.session()

    def append_row(self, img_source, img_link):
        data = json.dumps({"url": img_source})
        imgsource_req = self.session.post(self.url + 'add_imgsource', data=data)
        if imgsource_req.status_code == 200:
            data = json.dumps({"url": img_link, "imagesource_id": imgsource_req.json()['id']})
            img_req = self.session.post(self.url + 'add_img', data=data)
            if img_req.status_code == 200:
                print('Added to backend')
            else:
                print(f"Image failed: {img_req.content}")
        else:
            print(f"Image source failed: {imgsource_req.content}")


backend = BackendHandler()


class BaseScraper:
    _results = []
    """
    Базовый класс для скрейпера. В дальнейшем будет наследоваться
    у реализаций на asyncio, multiprocessing и threading
    """

    # передаем url с тегом и количество страниц для парсинга
    def __init__(self, base_url: str, start: int, end: int):
        self.base_url = base_url
        self.tag = unquote(self.base_url).split("/")[-1]
        self.page_range = range(start, end)
        self.session = requests.session()
        if not path.exists(f"images"):  # создает общую директорию
            makedirs(f"images")
        if (  # создает директорию под каждую из реализаций парсера в общей директории
            not type(self) is BaseScraper and
            not path.exists(f"images/{self}")
        ):
            makedirs(f"images/{self}")

    def extract_img_urls(self, page: int):
        with self.session.get(self.base_url + "/" + f"{page}", timeout=8) as req:
            if req.status_code == 200:
                soup_obj = BeautifulSoup(req.text, 'html.parser')
                # в старых постах изображения находятся в классе image, а не prettyPhotoLink
                if not (posts := soup_obj.findAll("a", class_="prettyPhotoLink")):
                    posts = soup_obj.findAll("div", class_="image")
                img_links = [tag.find("img").get("src") for tag in posts]
                if not img_links:
                    print("Did not find anything")
                    return []
                else:
                    return img_links
            else:
                print(f"Strangely, page {page} not found")
                return []

    def save_img(self, img: bytes):
        i = 0
        while path.exists(f"images/{self}/scraped_{self.tag}_{i}.jpeg"):
            i += 1
        try:
            with open(f"images/{self}/scraped_{self.tag}_{i}.jpeg", "wb") as f:
                # все изображения представлены в jpg, поэтому сохраняем их jpg
                f.write(img)
                print(f"Image saved as images/{self}/scraped_{self.tag}_{i}.jpeg")
        except IOError as e:
            print(f"An error occurred: {e}")

    def run(self):  # общий класс для замера времени и запуска
        start = time.time()
        self._calculate()
        end = time.time()
        # print(f"Executed {self}, took {end - start} seconds")
        BaseScraper._results.append(f"\nExecuted {self}, took {end - start} seconds")

    def fetch(self, link):
        print(f"Fetching {link}...")

    def parse(self, num):
        print(f"Parsing {num}...")


class ThreadScrape(BaseScraper):
    def __str__(self):
        return "ThreadScrape"

    def _thread_save(self, link):
        with self.session.get("http:" + link, timeout=8) as req:
            super().fetch(link)
            if req.status_code == 200:
                img = req.content
                self.save_img(img)
            else:
                print(f"Status {req.status_code}")

    def _thread_parse(self, num):
        img_links = self.extract_img_urls(num)
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS + 1) as executor:  # Limit to 4 worker threads
            for link in img_links:
                super().parse(num)
                executor.submit(self._thread_save, link)
                print("Preparing to fire append row...")
                backend.append_row(self.base_url + "/" + f"{num}", link)
                time.sleep(1.5)

    def _calculate(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:  # Limit to 4 worker threads
            for i in self.page_range:
                executor.submit(self._thread_parse, i)
                time.sleep(5)


class AsyncScrape(BaseScraper):
    def __str__(self):
        return "AsyncScrape"

    async def _async_save(self, link):
        with self.session.get("http:" + link, timeout=8) as req:
            print(f"Fetching {link}...")
            if req.status_code == 200:
                img = req.content
                self.save_img(img)
            else:
                print(f"Status {req.status_code}")

    async def _async_parse(self, num):
        img_links = self.extract_img_urls(num)
        tasks = []
        for link in img_links:  # processing links
            task = asyncio.create_task(self._async_save(link))
            await task
            backend.append_row(self.base_url + "/" + f"{num}", link)
            print(f"Parsing {num}...")
            time.sleep(1.5)

    async def _calculate_async(self):
        tasks = []
        for i in self.page_range:
            task = asyncio.create_task(self._async_parse(i))
            tasks.append(task)
            time.sleep(5)

        await asyncio.gather(*tasks)

    def _calculate(self):
        asyncio.run(self._calculate_async())


class ProcessScrape(BaseScraper):
    def __str__(self):
        return "ProcessScrape"

    def _process_save(self, link):
        with self.session.get("http:" + link, timeout=8) as req:
            if req.status_code == 200:
                img = req.content
                self.save_img(img)
            else:
                print(f"Status {req.status_code}")

    def _process_parse(self, num):
        img_links = self.extract_img_urls(num)
        processes = []
        for link in img_links:  # processing links
            p = Process(target=self._process_save, args=(link,))
            p.start()
            processes.append(p)
            backend.append_row(self.base_url + "/" + f"{num}", link)
            time.sleep(1.5)

        for p in processes:
            p.join()

    def _calculate(self):
        processes = []
        for i in self.page_range:
            p = Process(target=self._process_parse, args=(i,))
            p.start()
            processes.append(p)
            time.sleep(5)

        for p in processes:
            p.join()


def validate_input(cmd, url: str, start: str, end: str):
    if start.isdigit() and end.isdigit():
        start = int(start)
        end = int(end)
    else:
        raise TypeError("Can not convert str to int")
    if start > end and (start < 0 or end < 0):
        raise ValueError("Invalid page range")
    if url[-1] == "/":
        url = url[:-2]
        print("Trimmed the trailing '/' in the url")
    return url, start, end


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 4 and (refined_args := validate_input(*sys.argv)):
        # refined_args = ("https://joyreactor.cc/tag/%D0%BA%D0%BE%D1%82%D1%8D", 298, 300)
        a = ProcessScrape(*refined_args)
        b = AsyncScrape(*refined_args)
        c = ThreadScrape(*refined_args)
        a.run()
        b.run()
        c.run()
        for i in BaseScraper._results:
            print(i)
    else:
        print("Not enough parameters")
