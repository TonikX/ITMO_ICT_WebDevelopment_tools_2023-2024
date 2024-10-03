from multiprocessing import Pool
from time import time

first_number = 1
last_number = 1000000

NUMBER_OF_PROCESSES = 2
NUMBERS_FOR_PROCESSE = last_number // NUMBER_OF_PROCESSES

# Возвращает сумму чисел от start до end включительно
def calculate_sum(start: int, end: int):
    return sum(range(start, end+1))
    
# Основной поток
def processe_calculate_sum():
    # Создаём отдельные части на промежутке от первого до последнего числа
    params = [ (NUMBERS_FOR_PROCESSE * i + 1, NUMBERS_FOR_PROCESSE * (i + 1)) for i in range(NUMBER_OF_PROCESSES) ]
        
    # Передаём данные части в функцию
    with Pool(NUMBER_OF_PROCESSES) as pool:
        results = pool.starmap(calculate_sum, params) 
    
    print("Result(processe): " + str(sum(results)))


def non_processe_calculate_sum():
    results = calculate_sum(first_number, last_number)
    print("Result(non processe): " + str(results))


if __name__ == "__main__":
    n_tests = 10

    times = []
    for i in range(n_tests):
        start = time()
        processe_calculate_sum()
        end = time()
        times.append(end-start)
    result_avg_time = sum(times)/n_tests
    print("AVG time: " + str(result_avg_time))

    times = []
    for i in range(n_tests):
        start = time()
        non_processe_calculate_sum()
        end = time()
        times.append(end-start)
    result_avg_time = sum(times)/n_tests
    print("AVG time: " + str(result_avg_time))