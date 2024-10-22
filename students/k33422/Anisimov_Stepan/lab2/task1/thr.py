import threading 
from time import time


def calc(offset, task_count, res, index):
    sum = 0
    for i in range(1 + offset, 1000001, task_count):
        sum += i
    res[index] = sum


def main():
    thread_count = 10
    threads = []
    results = [0] * thread_count

    for i in range(thread_count):
        t = threading.Thread(target=calc, args=(i, thread_count, results, i))
        threads.append(t)
        t.start()

    for thr in threads:
        thr.join()
    
    print(sum(results))


if __name__ == "__main__":
    start_time = time()
    
    main()

    end_time = time()

    print(end_time - start_time)