import threading
from parser import parse_data
from save_data import save_to_db
import time

urls = [
    "https://www.litres.ru/author/kayl-simpson/",
    "https://www.litres.ru/author/robert-s-martin/",
    "https://www.litres.ru/author/darya-doncova/"
]

def parse_and_save(urls):
    for url in urls:
        author_info = parse_data(url)
        save_to_db(author_info)


def start():
    start_time = time.time()

    threads_cnt = 3
    size = len(urls) // threads_cnt
    batches = [urls[i:i + size] for i in range(0, len(urls), size)]

    threads = []
    for batch in batches:
        thread = threading.Thread(target=parse_and_save, args=(batch,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    execution_time = end_time - start_time

    print("threading")
    print(f"Время: {execution_time} с")


if __name__ == '__main__':
    start()
