import multiprocessing
import time

NUM_PROCESSES = 10
NUMBERS = 1000000

def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.put(partial_sum)

def get_range(i, chunk_size):
    start = i * chunk_size + 1
    end = start + chunk_size
    return start, end

def main():
    chunk_size = NUMBERS // NUM_PROCESSES
    result = multiprocessing.Queue()
    processes = []

    for i in range(NUM_PROCESSES):
        start, end = get_range(i, chunk_size)
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, result))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_sum = sum([result.get() for _ in range(result.qsize())])

    print("Sum of first 1000000 numbers using Multiprocessing:", final_sum)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Execution time using Multiprocessing:", time.time() - start_time)
