!!! example "Задание"
    Написать три различных программы на Python, использующие каждый из подходов: threading, 
    multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. 
    Разделите вычисления на несколько параллельных задач для ускорения выполнения.

=== "theading"

    ``` py
    import threading
    import time
    
    num = 5
    number = 1000000
    
    def calculate_sum(start, end, results, index):
        summ = 0
        for i in range(start, end + 1):
            summ += i
        results[index] = summ
    
    def Sum_threading():
        threads = []
        chunk_size = number // num
        result = [0] * num
        start_time = time.time()
    
        for i in range(num):
            start = i * chunk_size + 1
            end = start + chunk_size - 1
            thread = threading.Thread(target=calculate_sum, args=(start, end, result, i))
            threads.append(thread)
            thread.start()
    
        for thread in threads:
            thread.join()
    
        end_time = time.time()
    
        print(f"Сумма: {sum(result)}")
        print(f"Время: {end_time - start_time:.5f} секунд")
    
    if __name__ == "__main__":
        Sum_threading()

    ```
    Описание работы -  реализуем многопоточность через threading создавая несколько потоков в одном процессе
    
=== "multiprocessing"

    ``` py
    import multiprocessing
    import time
    
    num = 5
    number = 1000000
    
    def calculate_sum(start, end, results, index):
        summ = 0
        for i in range(start, end + 1):
            summ += i
        results[index] = summ
    
    def Sum_multiprocessing():
        processes = []
        chunk_size = number // num
        manager = multiprocessing.Manager()
        result = manager.list([0] * num)
        start_time = time.time()
    
        for i in range(num):
            start = i * chunk_size + 1
            end = start + chunk_size - 1
            process = multiprocessing.Process(target=calculate_sum, args=(start, end, result, i))
            processes.append(process)
            process.start()
    
        for process in processes:
            process.join()
    
        end_time = time.time()
    
        print(f"Сумма: {sum(result)}")
        print(f"Время: {end_time - start_time:.5f} секунд")
    
    if __name__ == "__main__":
        Sum_multiprocessing()

    ```
    Описание работы - реализуем одновременное выполнение через отдельные процессы

=== "async"

    ``` py
    import time
    import asyncio
    
    num = 5
    number = 1000000
    
    
    async def calculate_sum(start, end):
        return sum(range(start, end + 1))
    
    
    async def Sum_asyncio():
        tasks = []
        chunk_size = number // num
        start_time = time.time()
    
        for i in range(num):
            start = i * chunk_size + 1
            end = start + chunk_size - 1
            task = asyncio.create_task(calculate_sum(start, end))
            tasks.append(task)
    
        results = await asyncio.gather(*tasks)
        end_time = time.time()
    
        print(f"Сумма: {sum(results)}")
        print(f"Время: {end_time - start_time:.5f} секунд")
    
    
    if __name__ == "__main__":
        asyncio.run(Sum_asyncio())

    ```
    Описание работы -  реализуем мультипоточность через async приостанавливая выполнение процессов и возращаясь к ним потом


ВЫВОД

Время
- threading - 0.11сек
- multiprocessing - 0.35сек
- async - 0.04сек

- Threading лучше всего подходит для I/O-ориентированных задач, но ограничен GIL.
- Multiprocessing идеален для CPU-ориентированных задач и не подвержен GIL, но требует больше ресурсов.
- Async предоставляет эффективный способ обработки I/O без блокировок, но не подходит для задач, требующих интенсивных вычислений.

