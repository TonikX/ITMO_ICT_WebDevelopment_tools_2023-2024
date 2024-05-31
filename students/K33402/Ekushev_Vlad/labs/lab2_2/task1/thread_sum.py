import threading

TOTAL_NUMBERS = 1000000
THREAD_COUNT = 10

# Функция для вычисления суммы в заданном диапазоне
def calculate_range_sum(start, end, result_list):
    partial_sum = sum(range(start, end + 1))
    result_list.append(partial_sum)

def run_threads():
    threads = []
    result = []

    for i in range(THREAD_COUNT):
        start = i * (TOTAL_NUMBERS // THREAD_COUNT) + 1
        end = (i + 1) * (TOTAL_NUMBERS // THREAD_COUNT)
        thread = threading.Thread(target=calculate_range_sum, args=(start, end, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print("Общая сумма с использованием threading:", total_sum)

if __name__ == "__main__":
    import time

    start_time = time.time()
    run_threads()
    print("Время выполнения:", time.time() - start_time)
