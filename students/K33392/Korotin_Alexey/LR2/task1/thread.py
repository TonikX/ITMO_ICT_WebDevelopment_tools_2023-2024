import threading
from util import get_function_execution_time_sec


def calculate_sum(start, end, container: list):
    total = 0
    for num in range(start, end + 1):
        total += num

    container.append(total)


def main():
    num_threads = 4
    start = 1
    end = 1000000
    step = int(end / num_threads)

    threads = []
    container = []
    for i in range(num_threads):
        thread = threading.Thread(target=calculate_sum, args=(start + i * step, start + (i + 1) * step - 1, container))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Сумма чисел от 1 до 1000000: {sum(container)}")


if __name__ == "__main__":
    time_sec, *_ = get_function_execution_time_sec(main)
    print(f"Затраченное время - {time_sec:.3f} сек")


