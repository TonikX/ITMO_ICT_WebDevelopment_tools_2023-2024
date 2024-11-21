import threading
import time

def calculate_sum(start, end, results, index):
    total = sum(range(start, end))
    results[index] = total

def main():
    start_time = time.time()

    threads = []
    results = [0] * 4  # 4 подзадачи
    ranges = [(1, 250000), (250001, 500000), (500001, 750000), (750001, 1000001)]

    for i, (start, end) in enumerate(ranges):
        thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    end_time = time.time()

    print(f"Threading Sum: {total_sum}, Time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
