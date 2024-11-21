import multiprocessing
import time

def calculate_sum(start, end, queue):
    total = sum(range(start, end))
    queue.put(total)

def main():
    start_time = time.time()

    processes = []
    queue = multiprocessing.Queue()
    ranges = [(1, 250000), (250001, 500000), (500001, 750000), (750001, 1000001)]

    for start, end in ranges:
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = sum(queue.get() for _ in processes)
    end_time = time.time()

    print(f"Multiprocessing Sum: {total_sum}, Time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
