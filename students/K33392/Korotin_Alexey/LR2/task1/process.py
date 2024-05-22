import multiprocessing
from util import get_function_execution_time_sec


def calculate_sum(start, end, container: multiprocessing.Queue):
    total = 0
    for num in range(start, end + 1):
        total += num

    container.put(total)


def main():
    num_processes = 4
    start = 1
    end = 1000000
    step = int(end / num_processes)

    processes = []
    queue = multiprocessing.Queue()
    for i in range(num_processes):
        process = multiprocessing.Process(target=calculate_sum, args=(start + i * step, start + (i + 1) * step - 1, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Сумма чисел от 1 до 1000000: {sum(queue.get() for _ in range(num_processes))}")


if __name__ == "__main__":
    time_sec, *_ = get_function_execution_time_sec(main)
    print(f"Затраченное время - {time_sec:.3f} сек")

