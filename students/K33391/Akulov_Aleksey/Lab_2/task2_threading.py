from threading import Thread
import time

from common import URLS, parse_and_save


def main(urls):
    threads = []
    for url in urls:
        thread = Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start_time = time.time()
    main(URLS)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Threading time: {execution_time}")