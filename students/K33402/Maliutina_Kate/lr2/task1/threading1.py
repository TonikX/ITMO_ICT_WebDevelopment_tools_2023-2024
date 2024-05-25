import threading
from time import time


# функция подсчета суммы в заданном диапозоне
def calculate_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))
    # в result хранятся последовательно 5 сумм, которые вычисляются параллельно


def main():
    start_time = time()  # засекаем начальное время
    thread_count = 5  # выполняться программа будет в 5 потоков
    numbers_per_thread = 1_000_000 // thread_count  # в каждом потоке будет считаться сумма 200_000 чисел
    threads = list()  # создаем список потоков, где будут они храниться
    results = [0] * thread_count  # результирующий массив сумм

    for i in range(thread_count):  # проходимся циклом и запускаем потоки
        start = i * numbers_per_thread + 1  # первый индекс вычисляемого интервала
        end = start + numbers_per_thread - 1  # последний индекс вычисляемого интервала
        t = threading.Thread(target=calculate_sum, args=(start, end, results))  # создаем поток, передаем функцию и ее параметры
        threads.append(t)  # включаем поток в наш список, чтобы потом ждать его завершения
        t.start()  # запускаем поток

    for t in threads:  # в цикле ожидаем завершения всех потоков
        t.join()  # "присоединияемся" к ожиданию окончания

    total_sum = sum(results)  # считаем сумму тех 5 сумм
    end_time = time()  # засекаем конечное время
    print(f"Сумма: {total_sum}")  # выводим сумму
    print(f"Время выполнения: {end_time - start_time}")  # выводим время выполнения


if __name__ == "__main__":
    main()
