import multiprocessing

TOTAL_NUMBERS = 1000000
PROCESS_COUNT = 4

def compute_sum(start, end, result_queue):
    partial_sum = sum(range(start, end + 1))
    result_queue.put(partial_sum)

def run_processes():
    result_queue = multiprocessing.Queue()
    processes = []

    for i in range(PROCESS_COUNT):
        start = i * (TOTAL_NUMBERS // PROCESS_COUNT) + 1
        end = (i + 1) * (TOTAL_NUMBERS // PROCESS_COUNT)
        process = multiprocessing.Process(target=compute_sum, args=(start, end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = 0
    while not result_queue.empty():
        total_sum += result_queue.get()

    print("Общая сумма с использованием multiprocessing:", total_sum)

if __name__ == "__main__":
    import time

    start_time = time.time()
    run_processes()
    print("Время выполнения:", time.time() - start_time)

