import threading

# Функция, которая будет выполняться в каждом потоке для вычисления суммы
def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))  # Вычисление частичной суммы
    result.append(partial_sum)  # Добавление частичной суммы в общий результат

def main():
    num_threads = 4  # Количество потоков
    chunk_size = 1000000 // num_threads  # Размер порции данных для каждого потока
    threads = []  # Список для хранения потоков
    result = []  # Список для хранения частичных сумм

    # Создание и запуск потоков
    for i in range(num_threads):
        start = i * chunk_size + 1  # Начальное значение для порции данных
        end = (i + 1) * chunk_size + 1  # Конечное значение для порции данных
        thread = threading.Thread(target=calculate_sum, args=(start, end, result))  # Создание потока
        threads.append(thread)  # Добавление потока в список
        thread.start()  # Запуск потока

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    # Вычисление общей суммы
    total_sum = sum(result)
    print("Total sum:", total_sum)

if __name__ == "__main__":
    import time

    start_time = time.time()
    main()
    print("Execution time:", time.time() - start_time)