# Задание

### Цель работы
Понять отличия между потоками и процессами и понять, 
что такое ассинхронность в Python.

### Задачи работы
1. Написать три различных программы на Python, 
использующие каждый из подходов: threading, multiprocessing и async. 
Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. 
Разделить вычисления на несколько параллельных задач для ускорения выполнения.
2. Написать программу на Python для параллельного парсинга нескольких 
веб-страниц с сохранением данных в базу данных с использованием подходов 
threading, multiprocessing и async. Каждая программа должна парсить 
информацию с нескольких веб-сайтов, сохранять их в базу данных.



# Задание 1. Async

### Код

    import asyncio
    import time
    
    
    async def calculate_sum(start, end):
        total = sum(range(start, end + 1))
        return total
    
    
    async def main():
        n_tasks = 4
        tasks = []
        chunk_size = 1000000 // n_tasks
    
        for i in range(n_tasks):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size if i != n_tasks - 1 else 1000000
            tasks.append(calculate_sum(start, end))
    
        results = await asyncio.gather(*tasks)
        total_sum = sum(results)
        print(f"Total sum: {total_sum}")
    
    if __name__ == '__main__':
        start_time = time.time()
        asyncio.run(main())
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")

### Описание реализации

В программе используется модуль asyncio для для управления асинхронными 
операциями и time для измерения времени выполнения.

Функция calculate_sum является асинхронной, ключевое слово async указывает, 
что её выполнение может быть приостановлено и возобновлено. Функция 
вычисляет сумму всех целых чисел от начального значения start 
до конечного значения end.

В главной функции main определены следующие переменные:

 - n_tasks — количество создаваемых асинхронных задач;

 - tasks — список, в который будут сохраняться объекты задач;

 - chunk_size — диапазон чисел для каждой задачи, т.е. общий диапазон чисел разделяется между потоками и сохраняется в эту переменную.  

Далее в цикле создается каждая задача вызовом calculate_sum с правильными значениями начала и конца. Эти задачи добавляются в список tasks.
asyncio.gather используется для одновременного выполнения всех задач и ожидания их завершения. Он собирает их результаты в results.
Вычисляется и выводится общая сумма всех результатов из задач.

Скрипт фиксирует время начала, выполняет рутину main с помощью asyncio.run() и фиксирует время окончания после завершения.
В результате рассчитывается и выводится общее время выполнения.

### Async

Async использует один поток для управления выполнением задач, 
переключаясь между ними в точках, где одна задача ожидает ввода-вывода 
или другого события. Этот подход эффективен для задач, связанных с 
множеством операций ввода-вывода, позволяя обрабатывать тысячи соединений одновременно.

Ключевое слово async позволяет функциям приостанавливаться 
(с использованием await в более сложных сценариях), 
освобождая цикл событий для выполнения других задач. 
Здесь await используется с asyncio.gather для приостановки функции 
main до завершения всех задач.

# Задание 1. Multiprocessing

### Код

    import multiprocessing
    import time
    
    
    def calculate_sum(start, end, result_queue):
        total = sum(range(start, end + 1))
        result_queue.put(total)
    
    
    def main():
        n_processes = 4
        result_queue = multiprocessing.Queue()
        processes = []
        chunk_size = 1000000 // n_processes
    
        for i in range(n_processes):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size if i != n_processes - 1 else 1000000
            process = multiprocessing.Process(target=calculate_sum, args=(start, end, result_queue))
            processes.append(process)
            process.start()
    
        for process in processes:
            process.join()
    
        total_sum = 0
        while not result_queue.empty():
            total_sum += result_queue.get()
    
        print(f"Total sum: {total_sum}")
    
    
    if __name__ == '__main__':
        start_time = time.time()
        main()
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")

### Описание реализации
В программе используется модуль multiprocessing для параллельных 
вычислений с использованием нескольких процессов. Программа вычисляет 
сумму чисел от 1 до 1 000 000, разделяя задачу на четыре независимых 
процесса.

Реализация функции calculate_sum аналогчна предыдущей программе, кроме 
того, что есть очередь result_queue для сохранения результатов.

Здесь:

 - n_processes — количество процессов.

 - result_queue — очередь для сбора результатов от различных процессов.

 - processes — список с процессами.

Для каждого процесса создается объект multiprocessing.Process, которому передаются calculate_sum, начальные и конечные значения диапазона, а также очередь результатов. Затем процесс запускается.
После запуска всех процессов они синхронизируются с помощью метода join(), который гарантирует, что основной процесс main будет ожидать завершения всех дочерних процессов.
После завершения всех процессов суммируются результаты из result_queue.

### Multiprocessing

В multiprocessing каждый процесс работает в собственном адресном 
пространстве памяти. Такая программа может использовать несколько процессоров или 
ядер процессора, так как каждый процесс имеет свой собственный экземпляр 
интерпретатора Python. Для обмена данными между процессами используются 
межпроцессные коммуникации (например, очереди), что является более затратным по сравнению с 
потоками из-за необходимости сериализации и десериализации данных.


# Задание 1. Threading

### Код

    import threading
    import time
    
    
    def calculate_sum(start, end, result, index):
        total = sum(range(start, end + 1))
        result[index] = total
    
    
    def main():
        n_threads = 4
        results = [0] * n_threads
        threads = []
        chunk_size = 1000000 // n_threads
    
        for i in range(n_threads):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size if i != n_threads - 1 else 1000000
            thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
            threads.append(thread)
            thread.start()
    
        for thread in threads:
            thread.join()
    
        total_sum = sum(results)
        print(f"Total sum: {total_sum}")
    
    
    if __name__ == '__main__':
        start_time = time.time()
        main()
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")


### Описание реализации
Программа использует модуль threading для выполнения многопоточной 
обработки с целью распараллеливания вычисления суммы чисел от 1 до 
1 000 000.

Реализация функции calculate_sum аналогчна предыдущей программе, кроме 
того, что результаты вычислений записываются в result.

Здесь:

 - n_threads — количество потоков. 

 - results — массив для хранения результатов от каждого потока. 

 - threads — список, который будет хранить объекты потоков. 

В цикле для каждого потока создаётся и запускается объект threading.Thread, 
которому передаются функция calculate_sum и необходимые аргументы.
Метод join() используется для ожидания завершения всех потоков, что гарантирует, 
что основной поток будет ждать окончания работы всех дочерних потоков.
После завершения всех потоков суммируются результаты, хранящиеся в массиве results.

### Threading
В threading потоки разделяют одно и то же пространство памяти процесса, 
что упрощает передачу данных между потоками. Такой же принцип есть у multiprocessing.
Этот подход эффективен для операций ввода/вывода, 
потому что из-за GIL может одновременно выполняться только один поток, поэтому
в таких задачах это не приводит к увеличению производительности.


# Задание 2. Config

В этом файле хранятся константы с числом процессов, классы и теги для обработки содержания веб-страниц и
URL-адреса для парсинга. 

### Код

    URLS = [
    'https://skillbox.ru/media/management/kak-stat-prodaktmenedzherom-i-nuzhno-li-dlya-etogo-obrazovanie/',
    'https://skillbox.ru/media/management/produktovyy-analitik-chem-on-zanimaetsya-skolko-zarabatyvaet-i-kak-im-stat/',
    'https://skillbox.ru/media/code/qainzhener-kto-eto-chem-on-zanimaetsya-i-kak-im-stat/',
    'https://skillbox.ru/media/management/kto-takoy-restorator-skolko-on-zarabatyvaet-i-kak-im-stat/',
    ]

    NUM_THREADS = 4
    HTML_CLASS = 'stk-reset stk-theme_26309__style_large_header'
    HTML_TAG = 'h2'


# Задание 2. DataBaseConnection

В этом файле реализовано подключение к базе данных.

### Код

    import psycopg2
    
    
    class DataBaseConnection:
        INSERT_SQL = """INSERT INTO public.task(title, description, deadline, 
                                                created_date, priority, status, 
                                                category_id, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    
        @staticmethod
        def connect_to_database():
            conn = psycopg2.connect(
                dbname="tasks_db",
                user="postgres",
                password="12345",
                host="localhost",
                port="5433"
            )
            return conn


# Задание 2. Async

### Код

    import asyncio
    import aiohttp
    import time
    import config
    
    from connection import DataBaseConnection
    from bs4 import BeautifulSoup
    from datetime import date, timedelta
    
    
    async def parse_and_save(url, db_conn):
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    tasks = soup.find_all(config.HTML_TAG, class_=config.HTML_CLASS)
                    tasks = [task.text.strip().replace('\xa0', ' ') for task in tasks]
    
                    with db_conn.cursor() as cursor:
                        for task in tasks:
                            cursor.execute(DataBaseConnection.INSERT_SQL,
                                           (task, '', str(date.today()), str(date.today() + timedelta(7)),
                                            'high', 'to_do', 2, 3))
    
                    db_conn.commit()
        except Exception as e:
            print("Error:", e)
    
    
    async def process_url_list(url_list, conn):
        tasks = []
        for url in url_list:
            task = asyncio.create_task(parse_and_save(url, conn))
            tasks.append(task)
        await asyncio.gather(*tasks)
    
    
    async def main():
        urls = config.URLS
        num_threads = config.NUM_THREADS
        chunk_size = len(urls) // num_threads
        url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    
        db_conn = DataBaseConnection.connect_to_database()
        start_time = time.time()
    
        await asyncio.gather(*(process_url_list(chunk, db_conn) for chunk in url_chunks))
    
        db_conn.close()
        end_time = time.time()
    
        print(f"Execution time: {end_time - start_time:.2f} seconds")
    
    
    if __name__ == '__main__':
        asyncio.run(main())

### Описание

В программе используются асинхронные библиотеки asyncio и aiohttp. Программа 
параллельно парсит веб-страницы и записывает результат в базу данных. 

Асинхронная функция parse_and_save принимает URL-адрес для парсинга и объект соединения с базой данных. 
Она использует aiohttp для асинхронного получения HTML-страницы по указанному URL.
Далее содержимое страницы обрабатывается с помощью библиотеки BeautifulSoup для извлечения данных. 
Данные сохраняются в базу данных с помощью запроса.

Асинхронная функция process_url_list также принимает список URL-адресов и соединение с базой данных.
Для каждого URL создаётся асинхронная задача, которая вызывает parse_and_save.
asyncio.gather используется для одновременного выполнения всех задач.

В main загружается список URL-адресов из конфигурационного файла. 
Список делится на части для каждой задачи, далее устанавливается соединение с базой данных через DataBaseConnection.
Запускается параллельная обработка каждого чанка URL-адресов, используя asyncio.gather. 
Также Измеряется и выводится время выполнения программы от начала до окончания всех операций.

Программа максимально использует асинхронные операции для парсинга и обработки данных. 
Использование aiohttp для сетевых запросов и asyncio для управления асинхронными задачами минимизирует задержки и повышает производительность за счёт неблокирующего выполнения кода.
Асинхронное взаимодействие с базой данных обеспечивает быстрое сохранение результатов без замедления общего процесса выполнения.


# Задание 2. Multiprocessing

### Код

    import multiprocessing
    import time
    import config
    import requests
    
    from bs4 import BeautifulSoup
    from datetime import date, timedelta
    from connection import DataBaseConnection
    
    
    def parse_and_save(url):
        try:
            response = requests.get(url)
    
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                tasks = soup.find_all(config.HTML_TAG, class_=config.HTML_CLASS)
                tasks = [task.text.strip().replace('\xa0', ' ') for task in tasks]
            else:
                tasks = []
    
            with DataBaseConnection.connect_to_database() as db_conn:
                with db_conn.cursor() as cursor:
                    for task in tasks:
                        cursor.execute(DataBaseConnection.INSERT_SQL,
                                       (task, '', str(date.today()), str(date.today() + timedelta(7)),
                                        'high', 'to_do', 2, 3))
    
            db_conn.commit()
        except Exception as e:
            print("Error:", e)
    
    
    def process_url_list(url_queue):
        for url in url_queue:
            parse_and_save(url)
    
    
    def main():
        urls = config.URLS
        num_threads = config.NUM_THREADS
        chunk_size = len(urls) // num_threads
        url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    
        start_time = time.time()
        processes = []
    
        for chunk in url_chunks:
            process = multiprocessing.Process(target=process_url_list, args=(chunk,))
            process.start()
            processes.append(process)
    
        for process in processes:
            process.join()
    
        end_time = time.time()
    
        print(f"Execution time: {end_time - start_time:.2f} seconds")
    
    
    if __name__ == "__main__":
        main()

### Описание

Программа использует многопроцессорный подход для параллельного парсинга веб-страниц 
и сохранения извлечённых данных в базу данных. 

Функция parse_and_save принимает URL для парсинга и использует библиотеку requests для получения HTML-кода страницы.
Если HTTP-запрос успешен, ответ обрабатывается с помощью библиотеки BeautifulSoup. Извлеченные данные записываются в базу данных.

Функция process_url_list принимает очередь URL-адресов и последовательно обрабатывает каждый URL с помощью функции parse_and_save.

Функция main загружает список URL-адресов из конфигурационного файла и количество процессов. 
Далее делит список URL-адресов на равные части, размер которых зависит от указанного количества процессов.
Создаёт множество процессов, каждый из которых получает свою часть URL-адресов для обработки.
Запускает все процессы и ожидает их завершения. А также измеряет и выводит общее время выполнения операций.

В целом с помощью multiprocessing запросы выполяются параллельно, что ускоряет выполнение программы. 


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


# Результаты

|        | Threading | Multiprocessing | Asyncio  |
|--------|-----------|-----------------|----------|
| Task 1 | 0.01 sec  | 0.08 sec        | 0.01 sec |
| Task 2 | 1.05 sec  | 1.00 sec        | 0.54 sec |

### Вывод по заданию № 1
В реализации с threading потоки ограничиваются GIL. Но тут, возможно, за счет того, что вычисления простые GIL может не оказывать сильного влияния, поэтому получаем быстрое выполнение программы. Тут подход с Multiprocessing должен работать лучше, но при этом создание процессов, их управление, затраты на передачу данных между процессами через сериализацию и десериализацию могут приводить к дополнительным накладным расходам, возможно, из-за это время так увеличилось. Подход с asyncio тоже показывает хороший результат, тут у нас нет блокирующих операций и переключения контекста. 

## Вывод по заданию № 2
В целом в подходе с threading какое-то время может тратиться на управление потоками и переключение контекста, хотя ограничения GIL не так критичны для задач парсинга и записи в базу. Подход с multiprocessing позволяет полностью избежать проблем с GIL и процессы не зависят друг от друга. Асинхронное программирование с помощью asyncio идеально подходит для I/O-задач, таких как парсинг веб-страниц и взаимодействие с базами данных. Поскольку asyncio позволяет выполнять множество I/O операций, не блокируя основной поток выполнения.