import multiprocessing
import time


def calculate_partial_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.put(partial_sum)


def calculate_sum():
    num_processes = 2
    results = multiprocessing.Queue()

    processes = []
    start_time = time.time()
    chunk_size = 1000000 // num_processes
    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1 if i < num_processes - 1 else 1000001
        process = multiprocessing.Process(target=calculate_partial_sum, args=(start, end, results))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    total_sum = 0
    while not results.empty():
        total_sum += results.get()

    print("Total sum (Multiprocessing):", total_sum)
    print("Time taken:", end_time - start_time, "seconds")


if __name__ == "__main__":
    calculate_sum()
