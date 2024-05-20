import time
import threading

sm = 0
lock = threading.Lock()


def func():
    global sm
    with lock:
        for i in range(1000000):
            sm += i


if __name__ == '__main__':
    start_time = time.time()

    threads = [threading.Thread(target=func, daemon=True) for _ in range(10)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(sm)
