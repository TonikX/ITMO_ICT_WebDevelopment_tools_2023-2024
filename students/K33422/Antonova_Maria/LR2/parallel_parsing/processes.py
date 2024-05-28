from multiprocessing import Process
import requests
from bs4 import BeautifulSoup
import psycopg2

def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string

    # Соединение с базой данных
    conn = psycopg2.connect("dbname=baza3 user=moni password=123 host=localhost")
    cur = conn.cursor()

    # Сохранение заголовка в базу данных
    cur.execute("INSERT INTO pages (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    print(f"Title of {url}: {title}")

    cur.close()
    conn.close()

def main():
    urls = ["https://platffin.com", "https://lamoda.ru", "https://olsi-trade.ru"]
    processes = []

    for url in urls:
        process = Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    import time

    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")