from multiprocessing import Process
from task2.settings import URLS
from naive import parse_and_save
import time


def main():
    processes = []
    start_time = time.time()

    for url in URLS[:31]:
        process = Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(time.time() - start_time)


if __name__ == '__main__':
    main()