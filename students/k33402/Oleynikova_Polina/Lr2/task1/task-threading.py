import threading
import time


def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.append(total)


def main():
    start = 1
    end = 1000000
    n_threads = 4
    results = [0] * n_threads
    step = int(end / n_threads)

    threads = []    
    for i in range(n_threads):
        step_start = i * step + start
        step_end = (i + 1) * step + start if i != n_threads - 1 else end + 1
        thread = threading.Thread(target=calculate_sum, args=(step_start, step_end, results))
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