# Задание 1

*Каждый из подходов используется для решения задачи суммирования всех чисел от 1 до 1000000, разбивая вычисления на несколько параллельных задач для ускорения выполнения.*

## threading_sum.py

```python
import threading
import time

NUM_THREADS = 10
NUMBERS = 1000000

def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)

def get_range(i, chunk_size):
    start = i * chunk_size + 1
    end = start + chunk_size
    return start, end


def main():
    chunk_size = NUMBERS // NUM_THREADS
    result = []
    threads = []

    for i in range(NUM_THREADS):
        start, end = get_range(i, chunk_size)
        thread = threading.Thread(target=calculate_sum, args=(start, end, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_sum = sum(result)
    print("Sum of the first 1000000 numbers using Threading:", final_sum)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Execution time using Threading:", time.time() - start_time)
```
- **1-е время исполнения:** 0.02995443344116211
- **2-е время исполнения:** 0.034906625747680664
- **3-е время исполнения:** 0.029527902603149414

## multiprocessing_sum.py

```python
import multiprocessing
import time

NUM_PROCESSES = 10
NUMBERS = 1000000

def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.put(partial_sum)

def get_range(i, chunk_size):
    start = i * chunk_size + 1
    end = start + chunk_size
    return start, end

def main():
    chunk_size = NUMBERS // NUM_PROCESSES
    result = multiprocessing.Queue()
    processes = []

    for i in range(NUM_PROCESSES):
        start, end = get_range(i, chunk_size)
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, result))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_sum = sum([result.get() for _ in range(result.qsize())])

    print("Sum of first 1000000 numbers using Multiprocessing:", final_sum)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Execution time using Multiprocessing:", time.time() - start_time)
```
- **1-е время исполнения:** 0.2725694179534912
- **2-е время исполнения:** 0.22806882858276367
- **3-е время исполнения:** 0.22054171562194824

## asyncio_sum.py

```python
import asyncio
import time

NUM_TASKS = 10
NUMBERS = 1000000

async def calculate_sum(start, end):
    partial_sum = sum(range(start, end))
    return partial_sum

async def get_range(i, chunk_size):
    start = i * chunk_size + 1
    end = start + chunk_size
    return start, end

async def main():
    chunk_size = NUMBERS // NUM_TASKS
    tasks = []

    for i in range(NUM_TASKS):
        start, end = await get_range(i, chunk_size)
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    final_sum = sum(results)

    print("Sum of first 1000000 numbers using Asyncio:", final_sum)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print("Execution time using Asyncio:", time.time() - start_time)
```
- **1-е время исполнения:** 0.03049159049987793
- **2-е время исполнения:** 0.027925968170166016
- **3-е время исполнения:** 0.0325922966003418

## Выводы

|             | **Threading** | **Multiprocessing** | **Asyncio** |
| ----------- | ----------- | ----------------- | ------------- |
| 1           | 0.030     | 0.273           | 0.030       |
| 2           | 0.035     | 0.228           | 0.028       |
| 3           | 0.030     | 0.221           | 0.033       |
| **Avg**     | 0.031     | 0.240           | 0.030       |

- **Threading**: Время выполнения находится примерно на одном уровне с asyncio. Однако, Threading ограничен GIL, что может замедлить выполнение на многопроцессорных системах.
- **Multiprocessing**: требует больше времени из-за накладных расходов на управление процессами и обмен данными.
- **Asyncio**:  лучшую производительность благодаря эффективному использованию асинхронных операций без создания дополнительных процессов или потоков.