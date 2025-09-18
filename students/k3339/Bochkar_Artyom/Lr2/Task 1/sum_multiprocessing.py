import multiprocessing
import time


def calculate_sum(start, end, result_queue):
    """Вычисляет сумму чисел от start до end простым перебором"""
    partial_sum = 0
    for num in range(start, end + 1):
        partial_sum += num
    result_queue.put(partial_sum)


def multiprocessing_sum(N, num_processes=4):
    chunk_size = N // num_processes
    processes = []
    result_queue = multiprocessing.Queue()

    start_time = time.time()

    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_processes - 1 else N
        process = multiprocessing.Process(
            target=calculate_sum,
            args=(start, end, result_queue)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total = 0
    for _ in range(num_processes):
        total += result_queue.get()

    end_time = time.time()

    print(f"Multiprocessing sum: {total}")
    print(f"Time: {end_time - start_time:.4f} seconds")
    print(f"Processes used: {num_processes}")
    return end_time - start_time


if __name__ == "__main__":
    N = 1_000_000_000
    num_processes = 4
    print(f"Calculating sum from 1 to {N:,}")

    times = {}
    duration = multiprocessing_sum(N, num_processes)
    times[num_processes] = duration
    