import threading
import time

from plt_builder import paint

x = []
y = []

def calculate_sum_of_range(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)


def calculate_sum(border, threads_cnt):
    start_time = time.time()

    results = []
    threads = []

    cnt = border // threads_cnt
    for i in range(threads_cnt):
        start = i * cnt + 1
        end = (i + 1) * cnt + 1 if i < threads_cnt - 1 else border + 1
        thread = threading.Thread(target=calculate_sum_of_range, args=(start, end, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    result = sum(results)

    end_time = time.time()

    x.append(threads_cnt*1.0)
    y.append(end_time - start_time)

    print("Выполнено с использованием threading")

    print("Сумма: ", result)
    print("Кол-во потоков: ", threads_cnt)
    print("Время:", end_time - start_time, "с")


if __name__ == "__main__":
    border = 1000000
    for i in range(5, 6):
        calculate_sum(border, i)
    print(x, y)
    paint(x, y, "Сумма " + str(border) + " threading")

