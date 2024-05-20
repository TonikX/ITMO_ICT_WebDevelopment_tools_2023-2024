import multiprocessing
from time import time


def calculate_sum(start, end, queue):
    total_sum = sum(range(start, end + 1))
    queue.put(total_sum)


def main():
    n_processes = 4
    numbers_per_process = 1000000 // n_processes
    processes = []
    queue = multiprocessing.Queue()

    start_time = time()

    for i in range(n_processes):
        start = i * numbers_per_process + 1
        end = (i + 1) * numbers_per_process if i != n_processes - 1 else 1000000
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = 0
    while not queue.empty():
        total_sum += queue.get()

    print(f"Total Sum: {total_sum}")
    print(f"Multiprocessing time: {time() - start_time:.2f}")


if __name__ == "__main__":
    main()