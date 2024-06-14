from multiprocessing import Process, Queue
from time import time


def calculate_sum(start, end, result, index):
    print(f"started {index}")
    result.put(sum(range(start, end + 1)))
    print(f"finished {index}")


def main(process_count):
    numbers_per_process = 1_000_000 // process_count
    processes = list()
    q = Queue()

    start_time = time()
    for i in range(process_count):
        start = i * numbers_per_process + 1
        end = start + numbers_per_process - 1
        p = Process(target=calculate_sum, args=(start, end, q, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    result = 0
    while not q.empty():
        result += q.get()

    end_time = time()

    return result, end_time - start_time


if __name__ == "__main__":
    result, time = main(4)
    print(f"Result of execution 'multiprocessing': {result}")
    print(f"Time of execution 'multiprocessing': {time} seconds")
