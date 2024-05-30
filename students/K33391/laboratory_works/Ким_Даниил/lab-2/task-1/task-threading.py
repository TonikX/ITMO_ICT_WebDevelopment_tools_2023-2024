import threading
import time


def calculate_sum(start, end):
    return sum(range(start, end))


def worker(start, end, result, index):
    result[index] = calculate_sum(start, end)


def main():
    num_threads = 4
    n = 1000000
    step = n // num_threads
    threads = []
    results = [0] * num_threads

    start_time = time.time()
    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step + 1
        thread = threading.Thread(target=worker, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    end_time = time.time()
    print(f"Total sum is {total_sum}, computed in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
