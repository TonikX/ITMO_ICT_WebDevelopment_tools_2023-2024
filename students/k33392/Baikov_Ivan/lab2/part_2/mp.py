import multiprocessing
import time
import requests
from bs4 import BeautifulSoup

from conn import sion, init_db
from models import *
from urls import URLS


def parse_and_save(queue,url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print("Type of furniture: ", soup.find('title').text)
    title = soup.find('title').text
    products = soup.find_all('div', class_="product-card__info")
    for product in products:
        try:
            name = product.find('div', class_='product-card__title').get_text().strip()
            price = product.find('div', class_='product-card__buy-wrapper').find('div', class_='product-card__price-wrapper').get_text().strip()
            price_info = price.split('\n')
            price_info = price_info[0].strip()
            queue.put((title, name, price_info))
        except Exception as e:
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
            title, name, cost  = data[0], data[1], data[2]
            pesnya = Product(name=name, cost = cost, title=title)
            sion.add(pesnya)
            sion.commit()
    end_time = time.time()
    print(f"Multiprocessing time ': {end_time - start_time} seconds")