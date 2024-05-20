import threading
from time import time


def calculate_sum(start, end, result, index):
    total_sum = sum(range(start, end + 1))
    result[index] = total_sum


def main():
    n_threads = 4
    numbers_per_thread = 1000000 // n_threads
    threads = []
    results = [0] * n_threads

    start_time = time()

    for i in range(n_threads):
        start = i * numbers_per_thread + 1
        end = (i + 1) * numbers_per_thread if i != n_threads - 1 else 1000000
        thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    print(f"Total Sum: {total_sum}")
    print(f"Threading time: {time() - start_time:.2f}")


if __name__ == "__main__":
    main()
