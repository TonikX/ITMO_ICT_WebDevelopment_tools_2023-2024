from multiprocessing import Process, Queue
import requests
import sqlite3

urls = ["https://novabiom.ru/", "https://translate.google.com/?hl=ru&sl=tr&tl=ru&text=%C3%A7ok%20fazla%20spor&op=translate", "https://www.apple.com/"]

def parse_and_save(url, result):
    response = requests.get(url)
    if response.status_code == 200:
        title = response.text.split('<title>')[1].split('</title>')[0]
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pages (url, title) VALUES (?, ?)", (url, title))
        conn.commit()
        conn.close()
        result.put(title)

if __name__ == "__main__":
    result = Queue()
    processes = []
    for url in urls:
        process = Process(target=parse_and_save, args=(url, result))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not result.empty():
        print("Page title saved:", result.get())
