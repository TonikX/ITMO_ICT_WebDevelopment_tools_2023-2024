# Задание 2. Threading

### Код

    import threading
    import time
    import config
    import requests
    
    from connection import DataBaseConnection
    from bs4 import BeautifulSoup
    from datetime import date, timedelta
    
    
    def parse_and_save(url, db_conn):
        try:
            response = requests.get(url)
    
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                tasks = soup.find_all(config.HTML_TAG, class_=config.HTML_CLASS)
                tasks = [task.text.strip().replace('\xa0', ' ') for task in tasks]
            else:
                tasks = []
    
            with db_conn.cursor() as cursor:
                for task in tasks:
                    cursor.execute(DataBaseConnection.INSERT_SQL,
                                   (task, '', str(date.today()), str(date.today() + timedelta(7)),
                                    'high', 'to_do', 2, 3))
            db_conn.commit()
        except Exception as e:
            print("Error:", e)
    
    
    def process_url_list(url_queue, db_conn):
        for url in url_queue:
            parse_and_save(url, db_conn)
    
    
    def main():
        urls = config.URLS
        num_threads = config.NUM_THREADS
        chunk_size = len(urls) // num_threads
        url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    
        db_conn = DataBaseConnection.connect_to_database()
        start_time = time.time()
        threads = []
    
        for chunk in url_chunks:
            thread = threading.Thread(target=process_url_list, args=(chunk, db_conn))
            threads.append(thread)
            thread.start()
    
        for thread in threads:
            thread.join()
    
        end_time = time.time()
        db_conn.close()
    
        print(f"Execution time: {end_time - start_time:.2f} seconds")
    
    
    if __name__ == "__main__":
        main()

### Описание

Программа на Python использует многопоточность через модуль threading для параллельного парсинга 
веб-страниц и сохранения данных в базу данных.

Реализация программы аналогична программе с использованием multiprocessing, за исключением того, что
для каждого чанка URL-адресов создаётся поток, используя threading.Thread, с целью параллельной обработки.
