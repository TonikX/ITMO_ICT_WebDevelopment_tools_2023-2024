<<<<<<< Updated upstream
import threadingtask
=======
>>>>>>> Stashed changes
import time
import threading


def sum_numbers(start, end):
    partial_sum = sum(range(start, end))
    return partial_sum


def calculate_sum():
    thread_num = 4
    numbers_per_thread = 1000000 // thread_num

    partial_sums = []

    threads = []
    for i in range(thread_num):
        start = i * numbers_per_thread + 1
        end = start + numbers_per_thread if i < thread_num - 1 else 1000001
        thread = threading.Thread(target=lambda s, e: partial_sums.append(sum_numbers(s, e)), args=(start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(partial_sums)
    print("Total sum is", total_sum)


if __name__ == "__main__":
    start_time = time.time()
    calculate_sum()
    elapsed_time = time.time() - start_time
    print("Elapsed time:", elapsed_time)
