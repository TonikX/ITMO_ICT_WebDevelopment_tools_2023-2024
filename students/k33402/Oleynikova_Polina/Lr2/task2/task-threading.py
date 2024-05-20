import threading
import time
import config
from connection import DataBaseConnection
import requests
from bs4 import BeautifulSoup


def get_bio(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('div', class_='xZmPc')
    bio_container = text.find('div')
    if bio_container.em and bio_container.em.text:
        return bio_container.em.text
    if bio_container.text:
        return bio_container.text


def parse_and_save(url, db_conn):
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        tasks = soup.find_all('div', class_='CHPy6')
        for task in tasks:
            name = task.find('div', class_='dbENL').text + ' ' + task.find('div', class_='p1Gbz').text
            bio = get_bio('https://www.culture.ru' + task.a['href'])

            with db_conn.cursor() as cursor:
                    cursor.execute(DataBaseConnection.INSERT_SQL, (name, bio))

        db_conn.commit()
    except Exception as e:
        print("Error:", e)
        
        
def process_url_list(url_list, db_conn):
    for url in url_list:
        parse_and_save(url, db_conn)


def main():
    urls = config.URLS
    num_threads = config.NUM_THREADS
    chunk_size = len(urls) // num_threads
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    db_conn = DataBaseConnection.connect_to_database()
    
    threads = []
    for chunk in url_chunks:
        thread = threading.Thread(target=process_url_list, args=(chunk, db_conn))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    db_conn.close()


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")