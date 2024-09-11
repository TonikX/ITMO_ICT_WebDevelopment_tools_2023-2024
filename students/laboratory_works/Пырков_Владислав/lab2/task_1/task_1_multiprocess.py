import multiprocessing
import time

# функция, вычисляющая частичную сумму чисел от start до end и записывающая результат в общий список
def calculate_partial_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

# функция, распределяющая работу между процессами и собирающая результаты
def calculate_sum():
    total_processes = 5  # общее количество процессов
    n = 1000000  # верхняя граница диапазона
    process_list = []
    manager = multiprocessing.Manager()
    result = manager.list([0] * total_processes)  # общий список для хранения результатов

    # создаем процессы для вычисления частичных сумм
    for i in range(total_processes):
        start = i * (n // total_processes) + 1  # начало диапазона для текущего процесса
        end = (i + 1) * (n // total_processes) if i != total_processes - 1 else n  # конец диапазона для текущего процесса

        process = multiprocessing.Process(target=calculate_partial_sum, args=(start, end, result, i))
        process_list.append(process)
        process.start()  # запускаем процесс

    # ожидаем завершения всех процессов
    for process in process_list:
        process.join()

    total_sum = sum(result)  # суммируем результаты всех процессов
    return total_sum

if __name__ == '__main__':
    start_time = time.time()
    sum_result = calculate_sum()  # запускаем функцию
    end_time = time.time()
    print(f"sum: {sum_result}, time: {end_time - start_time} seconds")  # выводим результат и время выполнения
