from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup


def parse_and_save(url):
    headers = {
        'User-Agent': 'My User Agent 1.0',  # многие сайты не дают себя парсить ботам
    }

    response = requests.get(url, headers=headers)
    page = response.text
    soup = BeautifulSoup(page)
    title = soup.title.text
    return url, title


if __name__ == "__main__":
    n = 3
    with Pool(processes=n) as pool:
        work = [
            "https://www.gismeteo.ru/diary/4079/2023/2/",
            "https://www.w3schools.com/html/html_basic.asp",
            "https://www.javatpoint.com/simple-html-pages"
        ]
        result = pool.map(parse_and_save, work)
        print(result)
