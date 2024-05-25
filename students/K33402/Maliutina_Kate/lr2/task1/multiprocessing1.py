from multiprocessing import Process, Queue
from time import time


def calculate_sum(start, end, queue):
    queue.put(sum(range(start, end + 1)))


def main():
    start_time = time()
    queue = Queue()
    process_count = 5
    numbers_per_process = 1_000_000 // process_count
    processes = list()

    for i in range(process_count):
        start = i * numbers_per_process + 1
        end = start + numbers_per_process - 1
        p = Process(target=calculate_sum, args=(start, end, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total_sum = 0
    while not queue.empty():
        total_sum += queue.get()

    end_time = time()
    print(f"Сумма: {total_sum}")
    print(f"Время выполнения: {end_time - start_time}")


if __name__ == "__main__":
    main()
