from threading import Thread
import requests
from bs4 import BeautifulSoup
import psycopg2
import time

from common import pars_item, PAGES, URLS


def parse_and_save(url):
    url_f = url
    for page in PAGES:
        complete_url = f'{url_f}{page}'
        try:
            response = requests.get(complete_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса на страницу: {complete_url}\n{e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        items = soup.find_all('li', class_='s-item')

        for item in items:
            item_res = pars_item(item)
            print(item_res["name"], item_res["price"])


if __name__ == "__main__":
    start_time = time.time()
    for url in URLS:
        parse_and_save(url)
    end_time = time.time()
    execution_time = end_time - start_time