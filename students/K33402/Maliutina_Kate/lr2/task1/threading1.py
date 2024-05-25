import threading
from time import time


def calculate_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))


def main():
    start_time = time()
    thread_count = 5
    numbers_per_thread = 1_000_000 // thread_count
    threads = list()
    results = [0] * thread_count

    for i in range(thread_count):
        start = i * numbers_per_thread + 1
        end = start + numbers_per_thread - 1
        t = threading.Thread(target=calculate_sum, args=(start, end, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_sum = sum(results)
    end_time = time()
    print(f"Сумма: {total_sum}")
    print(f"Время выполнения: {end_time - start_time}")


if __name__ == "__main__":
    main()
