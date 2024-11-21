from concurrent.futures import ThreadPoolExecutor
import threading
import time
import math

result = 0
result_lock = threading.Lock()


def compute_sum(start, end):
    global result
    sm = sum(range(start, end+1))
    result_lock.acquire()
    result += sm
    result_lock.release()


def compute_with_threading(start, end, n_threads):
    global result
    result = 0

    with ThreadPoolExecutor() as executor:
        step = int(math.ceil((end - start) / n_threads))
        start_i = start
        while start_i <= end:
            end_i = min(start_i + step, end)
            executor.submit(compute_sum, start_i, end_i)
            start_i = end_i + 1

    return result


def measure(n_threads):
    start_time = time.perf_counter()
    res = compute_with_threading(1, 1000000, n_threads)
    elapsed = round(time.perf_counter() - start_time, 4)
    print(f"Threads: {n_threads}; time: {elapsed}; result: {res}")


if __name__ == "__main__":
    n_threads_list = [1, 5, 10, 20, 50, 100]
    for n_threads in n_threads_list:
        measure(n_threads)
