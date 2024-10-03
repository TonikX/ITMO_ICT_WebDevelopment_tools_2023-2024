import multiprocessing

import requests
import sqlite3
from bs4 import BeautifulSoup
import time


def parse_and_save(url, queue):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    musicians = soup.find_all("figure", class_="component-chartlist-item with-counter")
    for musician in musicians:
        container = musician.find("figcaption")
        artist_name = container.find("a", class_="track-artist").text
        music_name = container.find("a", class_="track-title").text

        queue.put((artist_name, music_name))


def worker(urls, queue):
    for url in urls:
        parse_and_save(url, queue)


def main():
    urls = [
        "https://www.americantop40.com/charts/top-40-238/september-28-2024/",
        "https://www.americantop40.com/charts/top-40-238/august-17-2024/",
        "https://www.americantop40.com/charts/top-40-238/july-13-2024/"
    ]
    num_processes = 3
    queue = multiprocessing.Queue()
    processes = []
    conn = sqlite3.connect('top.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT,
            music TEXT
        )
    ''')

    start_time = time.time()

    for i in range(num_processes):
        process = multiprocessing.Process(target=worker, args=(urls[i::num_processes], queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        artist_name, music_name = queue.get()
        cursor.execute('INSERT INTO artists (artist, music) VALUES (?, ?)', (artist_name, music_name))

    conn.commit()
    conn.close()
    end_time = time.time()
    print(f"Parsed and saved data in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()