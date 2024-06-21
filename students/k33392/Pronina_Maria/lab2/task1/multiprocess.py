import multiprocessing
import time


def calculate_sum(start_num, end_num, queue):
    res = sum(range(start_num, end_num))
    queue.put(res)


def main():
    n = 5
    total = 1000000
    chunk_size = total // n
    processes = list()
    queue = multiprocessing.Queue()

    for i in range(n):
        start_num = i * chunk_size + 1
        end_num = (i + 1) * chunk_size + 1
        process = multiprocessing.Process(target=calculate_sum, args=(start_num, end_num, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    res = 0
    while not queue.empty():
        res += queue.get()

    return res


if __name__ == "__main__":
    start_time = time.time()
    total_sum = main()
    result_time = time.time() - start_time
    print(f'Sum: {total_sum} \nTime: {result_time}')
