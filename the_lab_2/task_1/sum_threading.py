import threading
import time


def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.append(total)


def calculate():
    result = []
    threads = []

    for i in range(20):
        start = i * 50000 + 1
        end = (i + 1) * 50000 + 1
        thread = threading.Thread(target=calculate_sum, args=(start, end, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print("Total sum:", total_sum)


if __name__ == "__main__":
    start_time = time.time()
    calculate()
    print(f"Threading time: {time.time() - start_time}")
