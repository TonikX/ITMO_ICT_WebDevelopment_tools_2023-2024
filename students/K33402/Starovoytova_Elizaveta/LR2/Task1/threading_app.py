import threading
import time


def calculate_partial_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)


def calculate_sum():
    num_threads = 4
    results = []
    start_time = time.time()
    threads = []
    chunk_size = 1000000 // num_threads
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1 if i < num_threads - 1 else 1000001
        thread = threading.Thread(target=calculate_partial_sum, args=(start, end, results))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    end_time = time.time()
    total_sum = sum(results)
    print("Total sum (Threading):", total_sum)
    print("Time taken:", end_time - start_time, "seconds")


if __name__ == "__main__":
    calculate_sum()
