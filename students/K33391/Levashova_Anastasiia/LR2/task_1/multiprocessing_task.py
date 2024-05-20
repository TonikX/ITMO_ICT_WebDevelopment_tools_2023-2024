import multiprocessing
import time


def calculate_sum(start, end, result_queue):
    total = sum(range(start, end + 1))
    result_queue.put(total)


def main():
    n_processes = 4
    result_queue = multiprocessing.Queue()
    processes = []
    chunk_size = 1000000 // n_processes

    for i in range(n_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != n_processes - 1 else 1000000
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = 0
    while not result_queue.empty():
        total_sum += result_queue.get()

    print(f"Total sum: {total_sum}")


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
