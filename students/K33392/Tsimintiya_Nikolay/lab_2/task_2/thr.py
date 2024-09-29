import threading as t
import requests
from bs4 import BeautifulSoup

database = {}

work = [
    "https://www.gismeteo.ru/diary/4079/2023/2/",
    "https://www.w3schools.com/html/html_basic.asp",
    "https://www.javatpoint.com/simple-html-pages"
]
lock = t.Lock()


def parse_and_save(url):
    global database
    headers = {
        'User-Agent': 'My User Agent 1.0',  # многие сайты не дают себя парсить ботам
    }

    response = requests.get(url, headers=headers)
    page = response.text
    soup = BeautifulSoup(page)
    title = soup.title.text
    database[url] = title


def acquire_work():
    global work

    while True:
        lock.acquire()
        if work:
            url = work[0]
            work.pop(0)
            lock.release()
            parse_and_save(url)
        else:
            lock.release()
            return


def main(n: int):
    workers = []
    for _ in range(n):
        worker = t.Thread(target=acquire_work)
        workers.append(worker)
        worker.start()

    for w in workers:
        w.join()

    print(database)


main(3)