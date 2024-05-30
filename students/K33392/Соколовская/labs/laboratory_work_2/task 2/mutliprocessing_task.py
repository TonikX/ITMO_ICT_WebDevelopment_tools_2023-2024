import multiprocessing
from parser import parse_data
from save_data import save_to_db
import time

urls = [
    "https://www.litres.ru/author/kayl-simpson/",
    "https://www.litres.ru/author/robert-s-martin/",
    "https://www.litres.ru/author/darya-doncova/"
]

def parse_and_save(chunk):
    for url in chunk:
        author_info = parse_data(url)
        save_to_db(author_info)


def start():
    start_time = time.time()

    processes_cnt = len(urls)
    size = len(urls) // processes_cnt
    batches = [urls[i:i + size] for i in range(0, len(urls), size)]

    processes = []
    for batch in batches:
        process = multiprocessing.Process(target=parse_and_save, args=(batch,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    execution_time = end_time - start_time

    print("multiprocessing")
    print(f"Время: {execution_time} с")


if __name__ == '__main__':
    start()
