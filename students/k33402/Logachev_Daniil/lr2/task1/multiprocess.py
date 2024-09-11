import multiprocessing
import time

def calculate_partial_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

def calculate_sum():
    total_processes = 4
    n = 1000000
    process_list = []
    manager = multiprocessing.Manager()
    result = manager.list([0] * total_processes)
    step = n // total_processes

    for i in range(total_processes):
        start = i * step + 1
        end = (i + 1) * step if i != total_processes - 1 else n
        process = multiprocessing.Process(target=calculate_partial_sum, args=(start, end, result, i))
        process_list.append(process)
        process.start()

    for process in process_list:
        process.join()

    total_sum = sum(result)
    return total_sum


if __name__ == '__main__':
    start_time = time.time()
    sum_result = calculate_sum()
    end_time = time.time()
    print(f"Multiprocessing sum: {sum_result}, Time taken: {end_time - start_time} seconds")