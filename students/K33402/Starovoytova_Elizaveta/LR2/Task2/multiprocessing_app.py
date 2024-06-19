import multiprocessing
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
def parallel_parse_and_save(chunk):
    for url in chunk:
        author_info = parse_author_info(url)
        save_author_and_books_from_json(author_info)

# Функция для засечения времени исполнения и запуска парсинга
def measure_execution_time():
    start_time = time.time()

    # Разделение списка URL-адресов на равные части (chunks)
    num_processes = len(urls)
    chunk_size = len(urls) // num_processes
    chunks = [urls[i:i+chunk_size] for i in range(0, len(urls), chunk_size)]

    # Создание процессов для параллельного парсинга
    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(target=parallel_parse_and_save, args=(chunk,))
        processes.append(process)
        process.start()

    # Ожидание завершения всех процессов
    for process in processes:
        process.join()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

if __name__ == '__main__':
    # Вызов функции для засечения времени исполнения и запуска парсинга
    measure_execution_time()
