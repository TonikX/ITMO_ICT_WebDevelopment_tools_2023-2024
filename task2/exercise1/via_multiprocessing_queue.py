import multiprocessing
import time
import math


def compute_sum(start, end, queue):
    sm = sum(range(start, end + 1))
    queue.put(sm)


def compute_with_threading(start, end, n_threads):
    processes = []
    step = int(math.ceil((end - start) / n_threads))
    start_i = start
    queue = multiprocessing.Queue()
    while start_i <= end:
        end_i = min(start_i + step, end)
        process = multiprocessing.Process(
            target=compute_sum, args=[start_i, end_i, queue]
        )
        process.start()
        processes.append(process)
        start_i = end_i + 1

    for process in processes:
        process.join()

    result = 0
    while not queue.empty():
        result += queue.get()
    return result


def measure(n_threads):
    start_time = time.perf_counter()
    res = compute_with_threading(1, 1000000, n_threads)
    elapsed = round(time.perf_counter() - start_time, 4)
    print(f"Processes: {n_threads}; time: {elapsed}; result: {res}")


if __name__ == "__main__":
    n_threads_list = [1, 2, 5, 10, 30]
    for n_threads in n_threads_list:
        measure(n_threads)
