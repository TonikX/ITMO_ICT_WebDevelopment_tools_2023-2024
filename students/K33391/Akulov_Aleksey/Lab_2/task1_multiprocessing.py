from multiprocessing import Process, Queue
import time


def calculate_sum(start, end):
    return sum(range(start, end + 1))


def worker(start, end, results):
    partial_sum = calculate_sum(start, end)
    results.put(partial_sum)


def main_multiprocessing(total_numbers=1000000, ts=4):
    results = Queue()
    processes = []
    part = total_numbers // ts

    for i in range(ts):
        start = i * part + 1
        end = (i + 1) * part if i != ts - 1 else total_numbers
        process = Process(target=worker, args=(start, end, results))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    total_sum = 0
    while not results.empty():
        total_sum += results.get()

    print(f"Total sum is: {total_sum}")


if __name__ == "__main__":
    start_time = time.perf_counter()
    main_multiprocessing()
    end_time = time.perf_counter()
    print(f"Time: {end_time - start_time} sec")