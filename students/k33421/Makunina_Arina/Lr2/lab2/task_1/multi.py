from multiprocessing import Process, Array
from time import time


def calculate_sum(start, end, result, index):
    total = sum(range(start, end + 1))
    result[index] = total


def main():
    process_count = 10
    numbers_per_process = 100000 // process_count
    processes = []
    results = Array("i", process_count)

    start_time = time()
    for i in range(process_count):
        start = i * numbers_per_process + 1
        end = start + numbers_per_process - 1
        p = Process(target=calculate_sum, args=(start, end, results, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total_sum = sum(results)
    print(f"Total sum is {total_sum}")

    end_time = time()
    print(f"Multiprocessing time: {end_time - start_time}")


if __name__ == "__main__":
    main()
