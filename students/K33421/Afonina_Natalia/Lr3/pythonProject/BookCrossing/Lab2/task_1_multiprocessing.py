import time
from multiprocessing import Process, Manager


def sum_numbers(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)


def calculate_sum():
    process_num = 4
    numbers_per_process = 1000000 // process_num

    # Используем менеджер для общего списка результатов
    with Manager() as manager:
        partial_sums = manager.list()

        processes = []
        for i in range(process_num):
            start = i * numbers_per_process + 1
            end = start + numbers_per_process if i < process_num - 1 else 1000001
            process = Process(target=sum_numbers, args=(start, end, partial_sums))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        total_sum = sum(partial_sums)
        print("Total sum is", total_sum)


if __name__ == "__main__":
    start_time = time.time()
    calculate_sum()
    elapsed_time = time.time() - start_time
    print("Elapsed time:", elapsed_time)