import multiprocessing
import time


def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.put(total)


def main():
    start = 1
    end = 1000000
    n_processes = 4
    result_queue = multiprocessing.Queue()
    step = int(end / n_processes)

    processes = []    
    for i in range(n_processes):
        step_start = i * step + start
        step_end = (i + 1) * step + start if i != n_processes - 1 else end + 1
        process = multiprocessing.Process(target=calculate_sum, args=(step_start, step_end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = sum(result_queue.get() for _ in range(n_processes))
    print(f"Total sum: {total_sum}")


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")