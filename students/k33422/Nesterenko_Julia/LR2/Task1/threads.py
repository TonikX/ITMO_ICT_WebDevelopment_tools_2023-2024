import threading
from time import time


result = 0
lock = threading.Lock() 


def calculate_sum(i_from, i_to):
    global result
    lock.acquire()
    result += sum(range(i_from, i_to))
    lock.release() 


def check_n_splits(n):
    start = time()
    global result
    result = 0
    step = 10**6 // n
    chunks = [(i, i + step) for i in range(1, 10**6, step)]
    if chunks[-1][1] != 10**6:
        chunks[-1] = (chunks[-1][0], 10**6)

    threads = [threading.Thread(target=calculate_sum, args=chunk) 
                                for chunk in chunks]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Splits:", n)
    print("Result:", result)    
    print("Execution time:", time() - start)
    print()


if __name__ == "__main__":
    for n in range(2, 11):
        check_n_splits(n)
