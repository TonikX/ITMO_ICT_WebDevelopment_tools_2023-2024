import multiprocessing
import time
import requests
from bs4 import BeautifulSoup

from students.K33391.Volgin_Leonid.Lab_2.task_2.conn import init_db, sion
from models import *
from urls import URLS


def parse_and_save(queue,url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print("Listening music from: ",soup.find('title').text)
    title = soup.find('title').text
    songs = soup.find_all('div', class_="name_track")
    for song in songs:
        try:
            author = song.find('span', class_='artist').get_text()
            name = song.find('span', class_='song').get_text()
            #print(author,': ', name)
            queue.put((title, author, name))

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
            title, author, name  = data[0], data[1], data[2]
            pesnya = Song(name=name, author=author, title=title)
            sion.add(pesnya)
            sion.commit()
    end_time = time.time()
    print(f"Multiprocessing time ': {end_time - start_time} seconds")