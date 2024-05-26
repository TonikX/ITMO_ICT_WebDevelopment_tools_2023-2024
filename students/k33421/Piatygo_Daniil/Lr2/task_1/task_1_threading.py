import threading
from Lr2.mark_time import mark_time


def calculate_part_sum(start, end, results, idx):
    s = 0
    for i in range(start, end + 1):
        s += i
    results[idx] = s


@mark_time
def calculate_sum(n=1000000, n_threads=4):
    results = [0] * n_threads
    threads = []
    step = n // n_threads

    for i in range(n_threads):
        start = i * step + 1
        if i == n_threads - 1:
            end = n
        else:
            end = (i + 1) * step

        # Создаётся и запускается поток, в котором вычисляется частичная сумма
        thread = threading.Thread(
            target=calculate_part_sum, args=(start, end, results, i)
        )
        threads.append(thread)
        thread.start()

    # Дожидаемся завершения всех потоков
    # Нужно для того, чтобы результаты всех частичных сумм были записаны в results
    for thread in threads:
        thread.join()

    return sum(results)


if __name__ == "__main__":
    print(calculate_sum())
