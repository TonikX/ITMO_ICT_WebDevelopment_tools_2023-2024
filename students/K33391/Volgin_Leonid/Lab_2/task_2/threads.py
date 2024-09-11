import threading
import time
import requests
from bs4 import BeautifulSoup

from students.K33391.Volgin_Leonid.Lab_2.task_2.conn import init_db, sion
from models import *
from urls import URLS

lock = threading.Lock()

def parse_and_save(url):
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
            lock.acquire()
            pesnya = Song(name=name, author=author, title=title)
            sion.add(pesnya)
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