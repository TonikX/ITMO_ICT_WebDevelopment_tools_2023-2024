import threading
import time


def calculate_sum(start, end, result, index):
    total = sum(range(start, end + 1))
    result[index] = total


def main():
    n_threads = 4
    results = [0] * n_threads
    threads = []
    chunk_size = 1000000 // n_threads

    for i in range(n_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != n_threads - 1 else 1000000
        thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    print(f"Total sum: {total_sum}")


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
