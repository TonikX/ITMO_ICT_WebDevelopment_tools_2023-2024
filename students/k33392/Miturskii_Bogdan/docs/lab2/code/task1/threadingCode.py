import threading
import sys

def calculate_partial_sum(start, end, result, index):
    result[index] = sum(range(start, end))

def calculate_sum_threading(num_threads, total):
    step = total // num_threads
    threads = []
    results = [0] * num_threads

    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step + 1
        thread = threading.Thread(target=calculate_partial_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)

if __name__ == "__main__":
    import time
    num_threads = int(sys.argv[1])
    total = int(sys.argv[2])
    start_time = time.time()
    result = calculate_sum_threading(num_threads, total)
    end_time = time.time()
    print(f"Threading result: {result}, Time taken: {end_time - start_time} seconds")
