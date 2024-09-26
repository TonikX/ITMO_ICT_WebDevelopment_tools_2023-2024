# Лабораторная работа №2

Цель работы: понять отличия перечисленных понятий.

## Задача №1

Задача: Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных задач для ускорения выполнения.

Подробности задания:

Напишите программу на Python для каждого подхода: threading, multiprocessing и async.
Каждая программа должна содержать функцию calculate_sum(), которая будет выполнять вычисления.
Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова async/await и модуль asyncio.
Каждая программа должна разбить задачу на несколько подзадач и выполнять их параллельно.
Замерьте время выполнения каждой программы и сравните результаты.

## Ход выполнения работы

### sum_asyncio.py:
    import asyncio
    
    
    async def calculate_sum(start, end):
        return sum(range(start, end))
    
    
    async def main():
        chunk_size = 100000
        tasks = []
    
        for i in range(0, 1000000, chunk_size):
            tasks.append(calculate_sum(i+1, i+chunk_size+1))
    
        partial_sums = await asyncio.gather(*tasks)
        total_sum = sum(partial_sums)
        print("Конечный результат:", total_sum)
    
    if __name__ == "__main__":
        import time
        start_time = time.time()
        asyncio.run(main())
        print("Затраченное время:", time.time() - start_time)

### sum_multiprocessing.py:
     from multiprocessing import Process, Queue
    
    
    def calculate_sum(start, end, result_queue):
        partial_sum = sum(range(start, end))
        result_queue.put(partial_sum)
    
    
    def main():
        result_queue = Queue()
        processes = []
        chunk_size = 100000
    
        for i in range(0, 1000000, chunk_size):
            process = Process(target=calculate_sum, args=(i+1, i+chunk_size+1, result_queue))
            process.start()
            processes.append(process)
    
        for process in processes:
            process.join()
    
        total_sum = 0
        while not result_queue.empty():
            total_sum += result_queue.get()
    
        print("Конечный результат:", total_sum)
    
    if __name__ == "__main__":
        import time
        start_time = time.time()
        main()
        print("Затраченное время:", time.time() - start_time)

### sum_threading.py:
    import threading
    
    
    def calculate_sum(start, end, result):
        partial_sum = sum(range(start, end))
        result.append(partial_sum)
    
    
    def main():
        result = []
        threads = []
        chunk_size = 100000
    
        for i in range(0, 1000000, chunk_size):
            thread = threading.Thread(target=calculate_sum, args=(i + 1, i + chunk_size + 1, result))
            thread.start()
            threads.append(thread)
    
        for thread in threads:
            thread.join()
    
        total_sum = sum(result)
        print("Конечный результат:", total_sum)
    
    if __name__ == "__main__":
        import time
        start_time = time.time()
        main()
        print("Затраченное время:", time.time() - start_time)

## Результат

![Результат](images/lab_2/hZjRC26pZ6c.jpg)

![Результат](images/lab_2/mhhGFj5s8RE.jpg)

![Результат](images/lab_2/Zg7XxQDgGmw.jpg)


## Задача №2

Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

Подробности задания:

Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async.
Каждая программа должна содержать функцию parse_and_save(url), которая будет загружать HTML-страницу по указанному URL, парсить ее, сохранять заголовок страницы в базу данных и выводить результат на экран.
Используйте PostgreSQL или другую базу данных на ваш выбор для сохранения данных.
Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова async/await и модуль aiohttp для асинхронных запросов.
Создайте список нескольких URL-адресов веб-страниц для парсинга и разделите его на равные части для параллельного парсинга.
Запустите параллельный парсинг для каждой программы и сохраните данные в базу данных.
Замерьте время выполнения каждой программы и сравните результаты.

## Ход выполнения работы

### parse_asyncio.py:
    import asyncio
    import aiohttp
    import time
    import requests
    from bs4 import BeautifulSoup
    import asyncpg
    
    from task_2.db import init_db
    from models import *
    from urls import URLS
    import urllib.parse
    QUERY = """INSERT INTO flat (size, cost) VALUES ($1, $2)"""
    
    
    async def parse_and_save(url, db_pool):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(url) as response:
                    r = await response.text(encoding='utf-8', errors='ignore')
                    soup = BeautifulSoup(r, 'html.parser')
                    flats = soup.find_all('div', class_="catalog-block-item")
                    for flat in flats:
                        try:
                            size = flat.find('div', class_='catalog-block-item-name').get_text().strip()
                            print(size)
                            cost = flat.find('div', class_='catalog-block-item-price').find('div',class_='catalog-block-item-price-total hidden').get_text().strip()
                            await db_pool.fetch(QUERY, size, cost)
                        except Exception as e:
                            print(e)
        except Exception as ex:
            print(ex)
    
    async def main():
        tasks = []
        db_pool = await asyncpg.create_pool('postgresql://postgres:Scalapendra1219212712192127@localhost:5433/flat_db')
    
        for url in URLS:
            task = asyncio.create_task(parse_and_save(url, db_pool))
            tasks.append(task)
        await asyncio.gather(*tasks)
    
    
    if __name__ == '__main__':
        init_db()
        start_time = time.time()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
        end_time = time.time()
        print(f"Async time ': {end_time - start_time} seconds")
### parse_multiprocessing.py
    import multiprocessing
    import time
    import requests
    from bs4 import BeautifulSoup
    
    from task_2.db import ses, init_db
    from models import *
    from urls import URLS
    
    
    def parse_and_save(queue,url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        flats = soup.find_all('div', class_="catalog-block-item")
        for flat in flats:
            try:
                size = flat.find('div', class_='catalog-block-item-name').get_text().strip()
                cost = flat.find('div', class_='catalog-block-item-price').find('div',class_='catalog-block-item-price-total hidden').get_text().strip()
                queue.put((size, cost))
            except Exception:
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
                size, cost  = data[0], data[1]
                flat = Flat(size=size, cost = cost)
                ses.add(flat)
                ses.commit()
        end_time = time.time()
        print(f"Multiprocessing time ': {end_time - start_time} seconds")
### parse_threading.py
    import threading
    import time
    import requests
    from bs4 import BeautifulSoup
    
    from task_2.db import ses, init_db
    from models import *
    from urls import URLS
    
    lock = threading.Lock()
    
    def parse_and_save(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        flats = soup.find_all('div', class_="catalog-block-item")
        for flat in flats:
            try:
                size = flat.find('div', class_ = 'catalog-block-item-name').get_text().strip()
                print(size)
                cost = flat.find('div', class_='catalog-block-item-price').find('div', class_='catalog-block-item-price-total hidden').get_text().strip()
                print(cost)
                lock.acquire()
                res = Flat(size = size, cost = cost)
                ses.add(res)
                ses.commit()
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
## Результат

![Результат](images/lab_2/1.jpg)
![Результат](images/lab_2/2.jpg)
![Результат](images/lab_2/3.jpg)


