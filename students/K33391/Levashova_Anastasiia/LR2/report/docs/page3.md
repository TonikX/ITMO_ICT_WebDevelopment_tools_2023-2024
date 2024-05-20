# Задание 1. Threading

### Код

    import threading
    import time
    
    
    def calculate_sum(start, end, result, index):
        total = sum(range(start, end + 1))
        result[index] = total
    
    
    def main():
        n_threads = 4
        results = [0] * n_threads
        threads = []
        chunk_size = 1000000 // n_threads
    
        for i in range(n_threads):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size if i != n_threads - 1 else 1000000
            thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
            threads.append(thread)
            thread.start()
    
        for thread in threads:
            thread.join()
    
        total_sum = sum(results)
        print(f"Total sum: {total_sum}")
    
    
    if __name__ == '__main__':
        start_time = time.time()
        main()
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")


### Описание реализации
Программа использует модуль threading для выполнения многопоточной 
обработки с целью распараллеливания вычисления суммы чисел от 1 до 
1 000 000.

Реализация функции calculate_sum аналогчна предыдущей программе, кроме 
того, что результаты вычислений записываются в result.

Здесь:

 - n_threads — количество потоков. 

 - results — массив для хранения результатов от каждого потока. 

 - threads — список, который будет хранить объекты потоков. 

В цикле для каждого потока создаётся и запускается объект threading.Thread, 
которому передаются функция calculate_sum и необходимые аргументы.
Метод join() используется для ожидания завершения всех потоков, что гарантирует, 
что основной поток будет ждать окончания работы всех дочерних потоков.
После завершения всех потоков суммируются результаты, хранящиеся в массиве results.

### Threading
В threading потоки разделяют одно и то же пространство памяти процесса, 
что упрощает передачу данных между потоками. Такой же принцип есть у multiprocessing.
Этот подход эффективен для операций ввода/вывода, 
потому что из-за GIL может одновременно выполняться только один поток, поэтому
в таких задачах это не приводит к увеличению производительности.