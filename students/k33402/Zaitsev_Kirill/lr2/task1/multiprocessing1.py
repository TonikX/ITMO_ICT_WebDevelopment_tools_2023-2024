from multiprocessing import Process, Queue
from time import time


def calculate_sum(start, end, queue):
    # queue - очередь значений, куда мы складываем все подсчитанные суммы
    queue.put(sum(range(start, end + 1)))


def main():
    start_time = time()  # засекаем начальное время
    queue = Queue()  # создаем очередь для асинхронного сохранения значений
    process_count = 5  # выполняться программа будет в 5 процессов
    numbers_per_process = 1_000_000 // process_count  # в каждом процессе будет считаться сумма 200_000 чисел
    processes = list()

    for i in range(process_count):
        start = i * numbers_per_process + 1  # первый индекс вычисляемого интервала
        end = start + numbers_per_process - 1  # последний индекс вычисляемого интервала
        p = Process(target=calculate_sum, args=(start, end, queue))  # создаем процесс, передаем функцию и ее параметры
        processes.append(p)  # включаем процесс в наш список, чтобы потом ждать его завершения
        p.start()

    for p in processes:  # в цикле ожидаем завершения всех процессов
        p.join()  # "присоединияемся" к ожиданию окончания

    total_sum = 0  # объявляем общую сумму
    while not queue.empty():  # пока очередь не пуста и в ней есть значения
        total_sum += queue.get()  # складываем с общей суммой

    end_time = time()
    print(f"Сумма: {total_sum}")
    print(f"Время выполнения: {end_time - start_time}")


if __name__ == "__main__":
    main()
