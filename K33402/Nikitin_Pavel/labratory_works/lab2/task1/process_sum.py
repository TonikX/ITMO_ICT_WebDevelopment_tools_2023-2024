import multiprocessing

TOTAL = 1000000
NUM_PROCESSES = 4

def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end+1))
    result.put(partial_sum)

def main():
    result = multiprocessing.Queue()
    processes = []

    for i in range(NUM_PROCESSES):
        start = i * (TOTAL // NUM_PROCESSES) + 1
        end = (i + 1) * (TOTAL // NUM_PROCESSES)
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, result))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = 0
    while not result.empty():
        total_sum += result.get()

    print("Total sum using multiprocessing:", total_sum)

if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print("Execution time:", time.time() - start_time)
