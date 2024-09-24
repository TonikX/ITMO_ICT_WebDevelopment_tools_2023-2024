import threading

from handlers import (
    parse_all_urls,
    data_handlers
)


def parse_and_save():
    # Создаем потоки для обработки каждого URL
    threads = []
    for category, handler_func in data_handlers.items():
        url = f"https://async-lab.tiiny.site/{category}"
        print(url)
        thread = threading.Thread(target=parse_all_urls, args=(handler_func, url, 5))
        threads.append(thread)
        thread.start()

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    import time

    start_time = time.time()
    parse_and_save()
    print("Execution time:", time.time() - start_time)
