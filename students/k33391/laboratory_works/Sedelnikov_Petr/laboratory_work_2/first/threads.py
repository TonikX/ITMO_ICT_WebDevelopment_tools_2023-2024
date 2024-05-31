import threading
import time


def calculate_sum(start, end):
    return sum(range(start, end))


def worker(start, end, result, index):
    result[index] = calculate_sum(start, end)


def main():
    tasks_quantity = 4
    numbers = 1000000
    step = numbers // tasks_quantity
    threads = []
    results = [0] * tasks_quantity

    for i in range(tasks_quantity):
        start = i * step + 1
        end = (i + 1) * step + 1
        thread = threading.Thread(target=worker, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(results)
    print(f"Total: {total}")


if __name__ == "__main__":
    print("Threading")
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
