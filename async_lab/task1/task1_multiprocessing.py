from multiprocessing import Process, Queue

# Функция, которая будет выполняться в каждом процессе для вычисления суммы
def calculate_sum(start, end, result_queue):
    partial_sum = sum(range(start, end))  # Вычисление частичной суммы
    result_queue.put(partial_sum)  # Помещение частичной суммы в очередь результатов

def main():
    num_processes = 4  # Количество процессов
    chunk_size = 1000000 // num_processes  # Размер порции данных для каждого процесса
    processes = []  # Список для хранения процессов
    result_queue = Queue()  # Очередь для хранения частичных сумм

    # Создание и запуск процессов
    for i in range(num_processes):
        start = i * chunk_size + 1  # Начальное значение для порции данных
        end = (i + 1) * chunk_size + 1  # Конечное значение для порции данных
        process = Process(target=calculate_sum, args=(start, end, result_queue))  # Создание процесса
        processes.append(process)  # Добавление процесса в список
        process.start()  # Запуск процесса

    # Ожидание завершения всех процессов
    for process in processes:
        process.join()

    total_sum = 0
    while not result_queue.empty():
        total_sum += result_queue.get()

    print("Total sum:", total_sum)

if __name__ == "__main__":
    import time

    start_time = time.time()
    main()
    print("Execution time:", time.time() - start_time)

# каждый процесс имеет свое собственное пространство памяти, что означает,
# что данные не могут просто передаваться между процессами так же легко,
# как между потоками внутри одного процесса. Поэтому при использовании multiprocessing данные часто
# должны быть скопированы из одного процесса в другой,
# что может вызвать значительные накладные расходы на производительность,
# особенно при работе с большими объемами данных.
#
# Кроме того, создание и управление процессами требует больше ресурсов
# (например, время центрального процессора и память) по сравнению с потоками, которые являются более легковесными.
