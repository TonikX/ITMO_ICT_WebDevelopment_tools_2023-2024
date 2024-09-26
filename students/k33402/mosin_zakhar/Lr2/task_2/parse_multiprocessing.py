import multiprocessing
import time
import requests
from bs4 import BeautifulSoup

from task_2.db import ses, init_db
from models import *
from urls import URLS


def parse_and_save(queue,url):
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    flats = soup.find_all('div', class_="catalog-block-item")
    for flat in flats:
        try:
            size = flat.find('div', class_='catalog-block-item-name').get_text().strip()
            cost = flat.find('div', class_='catalog-block-item-price').find('div',class_='catalog-block-item-price-total hidden').get_text().strip()
            queue.put((size, cost))
        except Exception:
            pass
    queue.put(None)

if __name__ == '__main__':
    init_db()
    start_time = time.time()
    queue = multiprocessing.Queue()
    processes = []
    for url in URLS:
        process = multiprocessing.Process(target=parse_and_save,args=(queue, url))
        processes.append(process)
        process.start()
    len_proc = len(URLS)
    while len_proc>0:
        data = queue.get()
        if data is None:
            len_proc = len_proc - 1
        else:
            size, cost  = data[0], data[1]
            flat = Flat(size=size, cost = cost)
            ses.add(flat)
            ses.commit()
    end_time = time.time()
    print(f"Multiprocessing time ': {end_time - start_time} seconds")