import threading
from time import time

lock = threading.Lock()


def calculate_sum(i_from, i_to):
    global RESULT
    lock.acquire()
    RESULT += sum(range(i_from, i_to))
    lock.release()


if __name__ == "__main__":
    start = time()
    n = 4
    RESULT = 0
    step = 10**6 // n
    chunks = [(i, i + step) for i in range(1, 10**6, step)]
    if chunks[-1][1] != 10**6:
        chunks[-1] = (chunks[-1][0], 10**6)

    threads = [threading.Thread(target=calculate_sum, args=chunk) for chunk in chunks]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Result:", RESULT)
    print("Execution time:", time() - start)
