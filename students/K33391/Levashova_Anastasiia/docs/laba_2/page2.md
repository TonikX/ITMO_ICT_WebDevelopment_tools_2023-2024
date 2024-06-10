# Задание 1. Multiprocessing

### Код

    import multiprocessing
    import time
    
    
    def calculate_sum(start, end, result_queue):
        total = sum(range(start, end + 1))
        result_queue.put(total)
    
    
    def main():
        n_processes = 4
        result_queue = multiprocessing.Queue()
        processes = []
        chunk_size = 1000000 // n_processes
    
        for i in range(n_processes):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size if i != n_processes - 1 else 1000000
            process = multiprocessing.Process(target=calculate_sum, args=(start, end, result_queue))
            processes.append(process)
            process.start()
    
        for process in processes:
            process.join()
    
        total_sum = 0
        while not result_queue.empty():
            total_sum += result_queue.get()
    
        print(f"Total sum: {total_sum}")
    
    
    if __name__ == '__main__':
        start_time = time.time()
        main()
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")

### Описание реализации
В программе используется модуль multiprocessing для параллельных 
вычислений с использованием нескольких процессов. Программа вычисляет 
сумму чисел от 1 до 1 000 000, разделяя задачу на четыре независимых 
процесса.

Реализация функции calculate_sum аналогчна предыдущей программе, кроме 
того, что есть очередь result_queue для сохранения результатов.

Здесь:

 - n_processes — количество процессов.

 - result_queue — очередь для сбора результатов от различных процессов.

 - processes — список с процессами.

Для каждого процесса создается объект multiprocessing.Process, которому передаются calculate_sum, начальные и конечные значения диапазона, а также очередь результатов. Затем процесс запускается.
После запуска всех процессов они синхронизируются с помощью метода join(), который гарантирует, что основной процесс main будет ожидать завершения всех дочерних процессов.
После завершения всех процессов суммируются результаты из result_queue.

### Multiprocessing

В multiprocessing каждый процесс работает в собственном адресном 
пространстве памяти. Такая программа может использовать несколько процессоров или 
ядер процессора, так как каждый процесс имеет свой собственный экземпляр 
интерпретатора Python. Для обмена данными между процессами используются 
межпроцессные коммуникации (например, очереди), что является более затратным по сравнению с 
потоками из-за необходимости сериализации и десериализации данных.
