import threading
from time import time


def calculate_sum(start, end, result, index):
    total = sum(range(start, end + 1))
    result[index] = total


def main():
    thread_count = 10
    numbers_per_thread = 100000 // thread_count
    threads = []
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
    print(f"Total sum is {total_sum}")

    end_time = time()
    print(f"Threading time: {end_time - start_time}")


if __name__ == "__main__":
    main()
