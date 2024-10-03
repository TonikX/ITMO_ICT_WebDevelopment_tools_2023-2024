import threading
from time import time

first_number = 1
last_number = 1000000

NUMBER_OF_THREADS = 4
NUMBERS_FOR_THREAD = last_number // NUMBER_OF_THREADS

results = [0] * NUMBER_OF_THREADS 

# Возвращает сумму чисел от start до end включительно
def calculate_sum(start: int, end: int):
    return sum(range(start, end+1))

# Вызывает функцию calculate_sum и записывает в свою ячейку results
def worker(i: int):
    results[i] = calculate_sum(NUMBERS_FOR_THREAD * i + 1, NUMBERS_FOR_THREAD * (i + 1))
    
# Основной поток
def thread_calculate_sum():
    threads = []
    for i in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Result(thread): " + str(sum(results)))


def non_thread_calculate_sum():
    calculate_sum(first_number, last_number)
    print("Result(non thread): " + str(sum(results)))


if __name__ == "__main__":
    n_tests = 10

    times = []
    for i in range(n_tests):
        start = time()
        thread_calculate_sum()
        end = time()
        times.append(end-start)
    result_avg_time = sum(times)/n_tests
    print("AVG time: " + str(result_avg_time))

    times = []
    for i in range(n_tests):
        start = time()
        non_thread_calculate_sum()
        end = time()
        times.append(end-start)
    result_avg_time = sum(times)/n_tests
    print("AVG time: " + str(result_avg_time))