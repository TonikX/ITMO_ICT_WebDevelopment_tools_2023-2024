import threading
from parser import parse_author_info
from save_data import save_author_and_books_from_json
import time

# Список URL-адресов для парсинга
urls = [
    "https://www.litres.ru/author/patrik-king/",
    "https://www.litres.ru/author/vladimir-pozner/",
    "https://www.litres.ru/author/allan-dib/"
]

# Функция для параллельного парсинга и сохранения данных
def parallel_parse_and_save(urls):
    for url in urls:
        author_info = parse_author_info(url)
        save_author_and_books_from_json(author_info)

# Функция для засечения времени исполнения и запуска парсинга
def measure_execution_time():
    start_time = time.time()

    # Разделение списка URL-адресов на равные части
    num_threads = 3
    chunk_size = len(urls) // num_threads
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    # Запуск параллельного парсинга для каждой части
    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=parallel_parse_and_save, args=(chunk,))
        thread.start()
        threads.append(thread)

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

# Вызов функции для засечения времени исполнения и запуска парсинга
measure_execution_time()
