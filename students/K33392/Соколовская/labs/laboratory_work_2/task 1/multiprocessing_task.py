import multiprocessing
import time

from plt_builder import paint

x = []
y = []

def calculate_sum_of_range(start, end, result):
    partial_sum = sum(range(start, end))
    result.put(partial_sum)


def calculate_sum(border, processes_cnt):
    start_time = time.time()

    results = multiprocessing.Queue()

    processes = []
    cnt = border // processes_cnt
    for i in range(processes_cnt):
        start = i * cnt + 1
        end = (i + 1) * cnt + 1 if i < processes_cnt - 1 else border + 1
        process = multiprocessing.Process(target=calculate_sum_of_range, args=(start, end, results))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    result = 0
    while not results.empty():
        result += results.get()

    end_time = time.time()

    x.append(processes_cnt)
    y.append(end_time - start_time)

    print("Выполнено с использованием multiprocessing")

    print("Сумма: ", result)
    print("Время:", end_time - start_time, "с")


if __name__ == "__main__":
    border = 1000000
    for i in range(5, 6):
        calculate_sum(border, i)
    print(x, y)
    paint(x, y, "Сумма " + str(border) + " multiprocessing")
