import threading
import time
import requests
from bs4 import BeautifulSoup

from task_2.db import ses, init_db
from models import *
from urls import URLS

lock = threading.Lock()

def parse_and_save(url):
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    flats = soup.find_all('div', class_="catalog-block-item")
    for flat in flats:
        try:
            size = flat.find('div', class_ = 'catalog-block-item-name').get_text().strip()
            print(size)
            cost = flat.find('div', class_='catalog-block-item-price').find('div', class_='catalog-block-item-price-total hidden').get_text().strip()
            print(cost)
            lock.acquire()
            res = Flat(size = size, cost = cost)
            ses.add(res)
            ses.commit()
            lock.release()
        except Exception as e:
            pass

if __name__ == '__main__':

    init_db()
    start_time = time.time()
    threads = []
    for url in URLS:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    print(f"Threading time ': {end_time - start_time} seconds")