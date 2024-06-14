import threading
from time import time


def calculate_sum(start, end, result, index):
    print(f"started {index}")
    result[index] = sum(range(start, end + 1))
    print(f"finished {index}")


def main(thread_count):
    numbers_per_thread = 1_000_000 // thread_count
    threads = list()
    results = [0] * thread_count

    start_time = time()
    for i in range(thread_count):
        start = i * numbers_per_thread + 1
        end = start + numbers_per_thread - 1
        t = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_sum = sum(results)
    end_time = time()
    return total_sum, end_time - start_time


if __name__ == "__main__":
    result, time = main(4)
    print(f"Result of execution 'threading': {result}")
    print(f"Time of execution 'threading': {time} seconds")
