import threading
import time


def calculate_sum(start, stop, result):
    summary = 0
    for i in range(start, stop):
        summary += i
    result.append(summary)


def main():
    result = []
    threads = [threading.Thread(target=calculate_sum, args=(i, i + 10**4, result)) for i in range(1, 10**9, 10**4)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return sum(result)


time_start = time.time()
print(main())
print(time.time() - time_start)
# Время выполнения: 0.042426347732543945
# Время выполнения: 65.82674217224121
