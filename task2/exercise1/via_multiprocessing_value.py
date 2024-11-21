import multiprocessing
import time
import math


def compute_sum(start, end, res_value):
    sm = sum(range(start, end + 1))
    res_value.acquire()
    res_value.value += sm
    res_value.release()


def compute_with_threading(start, end, n_threads):
    processes = []
    values = []
    step = int(math.ceil((end - start) / n_threads))
    start_i = start
    value = multiprocessing.Value("q", 0)
    while start_i <= end:
        end_i = min(start_i + step, end)

        process = multiprocessing.Process(
            target=compute_sum, args=[start_i, end_i, value]
        )
        process.start()
        processes.append(process)
        start_i = end_i + 1

    for process in processes:
        process.join()

    return value.value


def measure(n_threads):
    start_time = time.perf_counter()
    res = compute_with_threading(1, 1000_000, n_threads)
    elapsed = round(time.perf_counter() - start_time, 4)
    print(f"Processes: {n_threads}; time: {elapsed}; result: {res}")


if __name__ == "__main__":
    n_threads_list = [1, 2, 5, 10, 30]
    for n_threads in n_threads_list:
        measure(n_threads)