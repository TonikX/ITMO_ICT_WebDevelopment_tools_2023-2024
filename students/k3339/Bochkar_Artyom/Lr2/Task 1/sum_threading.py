import threading
import time


def calculate_sum(start, end, result, index):
    """Вычисляет сумму чисел от start до end простым перебором"""
    partial_sum = 0
    for num in range(start, end + 1):
        partial_sum += num
    result[index] = partial_sum


def threading_sum(N, num_threads=4):
    chunk_size = N // num_threads
    threads = []
    results = [0] * num_threads

    start_time = time.time()

    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_threads - 1 else N
        thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total = sum(results)
    end_time = time.time()

    print(f"Threading sum: {total}")
    print(f"Time: {end_time - start_time:.4f} seconds")
    print(f"Threads used: {num_threads}")


if __name__ == "__main__":
    N = 1_000_000_000
    num_threads = 4
    print(f"Calculating sum from 1 to {N:,}")

    threading_sum(N, num_threads)