import multiprocessing
from time import time

def calculate_sum(start, end, result, index):
    total = sum(range(start, end + 1))
    result[index] = total

def main():
    processes = []
    num_processes = 10
    manager = multiprocessing.Manager()
    result = manager.list([0] * num_processes)
    total_numbers = 1000000
    chunk_size = total_numbers // num_processes
    start_time = time()

    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_processes - 1 else total_numbers
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, result, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = sum(result)
    print(f"Total Sum: {total_sum}")
    print(f"Time taken: {time() - start_time}")

if __name__ == "__main__":
    main()
