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

### async.py:
    
    import asyncio
    import time
    
    
    async def calculate_sum(start, end):
        return sum(range(start, end))
    
    async def main():
        tasks = 7
        total = 1000000
        step = total // tasks
        tasks_arr = []
    
        start = 1
        end = step + total % tasks + 1
    
        for i in range(tasks):
            task = asyncio.create_task(calculate_sum(start, end))
            start = end
            end = end + step
            tasks_arr.append(task)
    
        results = await asyncio.gather(*tasks_arr)
        total = sum(results)
        print(f"Total: {total}")
    
    
    if __name__ == "__main__":
        print("Async")
        start_time = time.time()
        asyncio.run(main())
        end_time = time.time()
        print(f"Time: {end_time - start_time} seconds")
        print("Гаусс справился бы быстрее")


### multik.py:

    import multiprocessing
    import time
    
    
    def calculate_sum(start, end):
        return sum(range(start, end))
    
    def worker(start, end, queue):
        queue.put(calculate_sum(start, end))
    
    if __name__ == '__main__':
        print("Multiprocessing")
        start_time = time.time()
    
        tasks = 7
        total = 1000000
        step = total // tasks
        tasks_arr = []
        queue = multiprocessing.Queue()
    
        start = 1
        end = step + total % tasks + 1
    
        for i in range(tasks):
            task = multiprocessing.Process(target=worker, args=(start, end, queue))
            start = end
            end = end + step
            tasks_arr.append(task)
            task.start()
    
        for task in tasks_arr:
            task.join()
    
        results = [queue.get() for i in tasks_arr]
        total_sum = sum(results)
        print(f"Total: {total_sum}")
    
        end_time = time.time()
        print(f"Time: {end_time - start_time} seconds")
        print("Гаусс справился бы быстрее")


### threads.py:
    import threading
    import time
    
    lock = threading.Lock()
    
    def calculate_sum(start, end):
        return sum(range(start, end))
    
    def worker(start, end, result):
        answer = calculate_sum(start, end)
        lock.acquire()
        result.append(answer)
        lock.release()
    
    
    print("Threading")
    start_time = time.time()
    
    tasks = 7
    total = 1000000
    step = total // tasks
    threads = []
    results = []
    
    start = 1
    end = step + total % tasks + 1
    
    for i in range(tasks):
        thread = threading.Thread(target=worker, args=(start, end, results))
        start = end
        end = end + step
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    total_answer = sum(results)
    print(f"Total: {total_answer}")
    
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
    print("Гаусс справился бы быстрее")

## Результат

![Результат](images/5.jpg)
############################################################
![Результат](images/6.jpg)
############################################################
![Результат](images/7.jpg)


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

### async.py:
    import asyncio
    import aiohttp
    import time
    import requests
    from bs4 import BeautifulSoup
    from sqlalchemy.dialects.postgresql import asyncpg
    
    from students.K33391.Volgin_Leonid.Lab_2.task_2.conn import init_db, sion
    from models import *
    from urls import URLS
    
    
    async def parse_and_save(url):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(url) as response:
                    r = await response.text()
                    soup = BeautifulSoup(r, 'html.parser')
                    print("Listening music from: ",soup.find('title').text)
                    title = soup.find('title').text
                    songs = soup.find_all('div', class_="name_track")
                    for song in songs:
                        try:
                            author = song.find('span', class_='artist').get_text()
                            name = song.find('span', class_='song').get_text()
                            #postgresql://postgres:Scalapendra1219212712192127@localhost:5433/song_database
                            async with asyncpg.connect(
                                    host='localhost',
                                    port=5433,
                                    user='postgres',
                                    password='Scalapendra1219212712192127',
                                    database='song_database'
                            ) as conn:
    
                                async with conn.cursor() as cur:
                                    sql = "INSERT INTO song (title, author, name) VALUES (%s, %s, %s)"
                                    data = [title, author, name]
                                    await cur.execute(sql, data)
                                    #await cur.execute("SELECT * FROM song")
                                    #rows = await cur.fetchall()
                                    #for row in rows:
                                    #    print(row)
    
    
                            #print(author,': ', name)
                            #pesnya = Song(name=name, author=author, title=title)
                            #sion.add(pesnya)
                            #sion.commit()
                        except Exception as e:
                            pass
        except Exception as ex:
            pass
    
    async def main():
        tasks = []
        for url in URLS:
            task = asyncio.create_task(parse_and_save(url))
            tasks.append(task)
        await asyncio.gather(*tasks)
    
    
    if __name__ == '__main__':
        init_db()
        start_time = time.time()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
        end_time = time.time()
        print(f"Async time ': {end_time - start_time} seconds")

### multik.py
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

### threads.py
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

## Результат

![Результат](images/1.jpg)
############################################################
![Результат](images/2.jpg)
############################################################
![Результат](images/3.jpg)

# Сравнение времени
## 1 задание
###async
![Результат](images/71.jpg)
###multi
![Результат](images/72.jpg)
###threads
![Результат](images/73.jpg)

Видно, что процессы работают в данном случае на порядок медленнее 

## 2 Задание
###async
![Результат](images/74.jpg)
###multi
![Результат](images/75.jpg)
###threads
![Результат](images/76.jpg)

В случае с парсингом вперед вырвалось asyncio за счёт асинхронного подключения к базе данных