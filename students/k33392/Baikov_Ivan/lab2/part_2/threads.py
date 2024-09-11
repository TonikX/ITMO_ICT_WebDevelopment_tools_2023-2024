import threading
import time
import requests
from bs4 import BeautifulSoup

from conn import sion, init_db
from models import *
from urls import URLS

lock = threading.Lock()

def parse_and_save(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print("Type of furniture: ",soup.find('title').text)
    title = soup.find('title').text
    products = soup.find_all('div', class_="product-card__info")
    for product in products:
        try:
            name = product.find('div', class_ = 'product-card__title').get_text().strip()
            price = product.find('div', class_='product-card__buy-wrapper').find('div',class_='product-card__price-wrapper').get_text().strip()
            price_info = price.split('\n')
            price_info = price_info[0].strip()
            lock.acquire()
            prod = Product(name = name, title = title, cost = price_info)
            sion.add(prod)
            sion.commit()
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