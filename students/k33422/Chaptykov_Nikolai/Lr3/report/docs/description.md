# Импорты, базовый скрапер
Необходимые библиотеки для скрипта:
```Python
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
```
Напишем базовый скрапер/парсер:
```Python
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


class BaseScraper:
    _results = [] # хранит результаты времени выполнения
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
```