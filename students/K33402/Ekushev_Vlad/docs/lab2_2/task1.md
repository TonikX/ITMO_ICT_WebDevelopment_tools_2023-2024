# Задание 1

Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async.
Каждая программа должна решать считать сумму всех чисел от 1 до 1000000.
Разделите вычисления на несколько параллельных задач для ускорения выполнения.

# async

```Python title="async_sum.py"
import asyncio

TOTAL_NUMBERS = 1000000
TASK_COUNT = 10

async def compute_range_sum(start, end):
    return sum(range(start, end + 1))

async def run_tasks():
    tasks = []
    step = TOTAL_NUMBERS // TASK_COUNT

    for i in range(TASK_COUNT):
        range_start = i * step + 1
        range_end = (i + 1) * step
        tasks.append(compute_range_sum(range_start, range_end))

    results = await asyncio.gather(*tasks)
    final_sum = sum(results)
    print("Общая сумма с использованием async/await:", final_sum)

if __name__ == "__main__":
    import time

    start_time = time.time()
    asyncio.run(run_tasks())
    print("Время выполнения:", time.time() - start_time)
```

# process

```Python title="process_sum.py"
import multiprocessing

TOTAL_NUMBERS = 1000000
PROCESS_COUNT = 4

def compute_sum(start, end, result_queue):
    partial_sum = sum(range(start, end + 1))
    result_queue.put(partial_sum)

def run_processes():
    result_queue = multiprocessing.Queue()
    processes = []

    for i in range(PROCESS_COUNT):
        start = i * (TOTAL_NUMBERS // PROCESS_COUNT) + 1
        end = (i + 1) * (TOTAL_NUMBERS // PROCESS_COUNT)
        process = multiprocessing.Process(target=compute_sum, args=(start, end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = 0
    while not result_queue.empty():
        total_sum += result_queue.get()

    print("Общая сумма с использованием multiprocessing:", total_sum)

if __name__ == "__main__":
    import time

    start_time = time.time()
    run_processes()
    print("Время выполнения:", time.time() - start_time)
```

# threading

```Python title="thread_sum.py"
import threading

TOTAL_NUMBERS = 1000000
THREAD_COUNT = 10

# Функция для вычисления суммы в заданном диапазоне
def calculate_range_sum(start, end, result_list):
    partial_sum = sum(range(start, end + 1))
    result_list.append(partial_sum)

def run_threads():
    threads = []
    result = []

    for i in range(THREAD_COUNT):
        start = i * (TOTAL_NUMBERS // THREAD_COUNT) + 1
        end = (i + 1) * (TOTAL_NUMBERS // THREAD_COUNT)
        thread = threading.Thread(target=calculate_range_sum, args=(start, end, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print("Общая сумма с использованием threading:", total_sum)

if __name__ == "__main__":
    import time

    start_time = time.time()
    run_threads()
    print("Время выполнения:", time.time() - start_time)
```

# Результаты и вывод

| Метод       | Время                   |
| ----------- | ----------------------- |
| `async`     | 0.005821943283081055 s |
| `process`   | 0.010497093200683594 s |
| `thread`    | 0.006220579147338867 s |

Несмотря на то, что количество итераций в цикле сравнительно невелико (1 000 000), использование многопоточности или многопроцессности не улучшает производительность программы. Это связано с тем, что время, затрачиваемое на создание и управление потоками или процессами (context switching), превышает время, необходимое для последовательного вычисления суммы в одном потоке.

Однако при существенном увеличении количества итераций использование многопоточности или процессов может значительно повысить производительность, поскольку время, затрачиваемое на создание и управление потоками или процессами, становится незначительным по сравнению со временем, необходимым для вычисления суммы последовательно.