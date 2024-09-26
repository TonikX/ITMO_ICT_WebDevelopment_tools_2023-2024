import multiprocessing
import time


def calculate_sum(start, end):
    return sum(range(start, end))


def worker(start, end, queue):
    queue.put(calculate_sum(start, end))


def main():
    num_processes = 4
    n = 1000000
    step = n // num_processes
    processes = []
    queue = multiprocessing.Queue()

    start_time = time.time()
    for i in range(num_processes):
        start = i * step + 1
        end = (i + 1) * step + 1
        process = multiprocessing.Process(target=worker, args=(start, end, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = sum(queue.get() for _ in range(num_processes))
    end_time = time.time()
    print(f"Total sum is {total_sum}, computed in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
