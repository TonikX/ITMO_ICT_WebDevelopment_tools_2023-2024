import multiprocessing
import sys

def calculate_partial_sum(start, end):
    return sum(range(start, end))

def calculate_sum_multiprocessing(num_processes, total):
    step = total // num_processes
    pool = multiprocessing.Pool(processes=num_processes)

    tasks = [(i * step + 1, (i + 1) * step + 1) for i in range(num_processes)]
    results = pool.starmap(calculate_partial_sum, tasks)

    return sum(results)

if __name__ == "__main__":
    import time
    num_processes = int(sys.argv[1])
    total = int(sys.argv[2])
    start_time = time.time()
    result = calculate_sum_multiprocessing(num_processes, total)
    end_time = time.time()
    print(f"Multiprocessing result: {result}, Time taken: {end_time - start_time} seconds")
