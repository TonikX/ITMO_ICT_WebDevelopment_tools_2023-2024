import threading
import requests
import sqlite3

urls = ["https://novabiom.ru/", "https://translate.google.com/?hl=ru&sl=tr&tl=ru&text=%C3%A7ok%20fazla%20spor&op=translate", "https://www.apple.com/"]

def parse_and_save(url):
    response = requests.get(url)
    if response.status_code == 200:
        title = response.text.split('<title>')[1].split('</title>')[0]
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pages (url, title) VALUES (?, ?)", (url, title))
        conn.commit()
        conn.close()
        print("Page title saved:", title)

if __name__ == "__main__":
    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
