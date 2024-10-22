from multiprocessing import Process, Queue
from time import time


def calc(offset, task_count, queue):
    sum = 0
    for i in range(1 + offset, 1000001, task_count):
        sum += i
    queue.put(sum)


def main():
    process_count = 10
    processes = []
    results = Queue()

    for i in range(process_count):
        p = Process(target=calc, args=(i, process_count, results))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    
    total = 0
    while not results.empty():
        total += results.get()
    
    print(total)


if __name__ == "__main__":
    start_time = time()

    main()

    end_time = time()
    print(end_time - start_time)