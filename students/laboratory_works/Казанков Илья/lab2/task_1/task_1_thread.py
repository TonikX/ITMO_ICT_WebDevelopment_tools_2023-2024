import threading
import time

# функция, вычисляющая частичную сумму чисел от start до end и записывающая результат в общий список
def calculate_partial_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

# функция, распределяющая работу между потоками и собирающая результаты
def calculate_sum():
    total_threads = 5  # общее количество потоков
    n = 1000000  # верхняя граница диапазона
    thread_list = []
    result = [0] * total_threads  # общий список для хранения результатов

    # создаем потоки для вычисления частичных сумм
    for i in range(total_threads):
        start = i * (n // total_threads) + 1  # начало диапазона для текущего потока
        end = (i + 1) * (n // total_threads) if i != total_threads - 1 else n  # конец диапазона для текущего потока

        thread = threading.Thread(target=calculate_partial_sum, args=(start, end, result, i))
        thread_list.append(thread)
        thread.start()  # запускаем поток

    # ожидаем завершения всех потоков
    for thread in thread_list:
        thread.join()

    total_sum = sum(result)  # суммируем результаты всех потоков
    return total_sum

start_time = time.time()
sum_result = calculate_sum()  # запускаем функцию
end_time = time.time()
print(f"sum: {sum_result}, time: {end_time - start_time} seconds")  # выводим результат и время выполнения
