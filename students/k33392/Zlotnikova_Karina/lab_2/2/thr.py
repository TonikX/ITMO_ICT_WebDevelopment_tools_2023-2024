import threading
import time
import requests
from bs4 import BeautifulSoup
from db.db import s, init_db
from db.models import Vinil
from db.url import urls

lock = threading.Lock()

def parse_and_save(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    vinils = soup.find_all('div', class_="album")
    for vinil in vinils:
        try:
            name = vinil.find('div', class_ = 'album_cont').find('h4', class_ = 'album_title').find('a')
            start_author = str(name).find('>') + 1
            end_author =str(name).find('<br')
            author = str(name)[start_author:end_author].strip()
            start_album = str(name).find('<br/>') + 5
            end_album = str(name).find('</a')
            album_title = str(name)[start_album:end_album].strip()
            cost = vinil.find('div', class_ = 'album_footer').find('div', class_ = 'price').get_text().strip()
            lock.acquire()
            vin = Vinil(name = album_title, author = author, cost = cost)
            s.add(vin)
            s.commit()
            lock.release()
        except Exception:
            pass

if __name__ == '__main__':

    init_db()
    start_time = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    print(f"Threads': {end_time - start_time} s.")