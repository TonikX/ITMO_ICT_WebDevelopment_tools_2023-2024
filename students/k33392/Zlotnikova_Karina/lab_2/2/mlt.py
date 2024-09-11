import multiprocessing
import time
import requests
from bs4 import BeautifulSoup

from db.db import init_db, s
from db.models import Vinil
from db.url import urls


def parse_and_save(queue,url):
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
            queue.put((author, album_title, cost))
        except Exception:
            pass
    queue.put(None)

if __name__ == '__main__':
    init_db()
    start_time = time.time()
    queue = multiprocessing.Queue()
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=parse_and_save,args=(queue, url))
        processes.append(process)
        process.start()
    len_proc = len(urls)
    while len_proc>0:
        data = queue.get()
        if data is None:
            len_proc = len_proc - 1
        else:
            author, album_title, cost  = data[0], data[1], data[2]
            vinil = Vinil(name=album_title, cost = cost, author=author)
            s.add(vinil)
            s.commit()
    end_time = time.time()
    print(f"Multiprocessing': {end_time - start_time} s.")