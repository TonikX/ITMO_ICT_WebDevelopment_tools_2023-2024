# Задание 1 

## Релазиация на asyncIO

Код:
```python
import asyncio
import math
import time


async def compute_sum(start, end):
    return sum(range(start, end + 1))


async def compute_with_threading(start, end, n_funcs):
    coroutines = []
    step = int(math.ceil((end - start) / n_funcs))
    start_i = start
    while start_i <= end:
        end_i = min(start_i + step, end)
        coroutine = compute_sum(start_i, end_i)
        coroutines.append(coroutine)
        start_i = end_i + 1

    gather_coroutine = asyncio.gather(*coroutines)
    partial_sums = await gather_coroutine
    result_sum = sum(partial_sums)
    return result_sum


async def measure(n_funcs):
    start_time = time.perf_counter()
    res = await compute_with_threading(1, 1000000, n_funcs)
    elapsed = round(time.perf_counter() - start_time, 4)
    print(f"Async functions: {n_funcs}; time: {elapsed}; result: {res}")


async def main():
    n_funcs_list = [1, 5, 10, 20, 50, 100, 1000]
    for n_funcs in n_funcs_list:
        await measure(n_funcs)


if __name__ == "__main__":
    asyncio.run(main())
```

Результат:
```
Async functions: 1; time: 0.0793; result: 500000500000
Async functions: 5; time: 0.067; result: 500000500000
Async functions: 10; time: 0.1418; result: 500000500000
Async functions: 20; time: 0.0961; result: 500000500000
Async functions: 50; time: 0.1274; result: 500000500000
Async functions: 100; time: 0.1254; result: 500000500000
Async functions: 1000; time: 0.0747; result: 500000500000
```

Вывод: 

Видим, что увеличение функций не приводит к приросту мощности, потому что в
нашей программе нет операций с ожиданием результат, вопрос заключается только 
в вычислительной мощности


## Реализация на threading

Код:
```python
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import math

result = 0
result_lock = threading.Lock()


def compute_sum(start, end):
    global result
    sm = sum(range(start, end+1))
    result_lock.acquire()
    result += sm
    result_lock.release()


def compute_with_threading(start, end, n_threads):
    global result
    result = 0

    with ThreadPoolExecutor() as executor:
        step = int(math.ceil((end - start) / n_threads))
        start_i = start
        while start_i <= end:
            end_i = min(start_i + step, end)
            executor.submit(compute_sum, start_i, end_i)
            start_i = end_i + 1

    return result


def measure(n_threads):
    start_time = time.perf_counter()
    res = compute_with_threading(1, 1000000, n_threads)
    elapsed = round(time.perf_counter() - start_time, 4)
    print(f"Threads: {n_threads}; time: {elapsed}; result: {res}")


if __name__ == "__main__":
    n_threads_list = [1, 5, 10, 20, 50, 100]
    for n_threads in n_threads_list:
        measure(n_threads)

```

Результат:
```
Threads: 1; time: 0.0827; result: 500000500000
Threads: 5; time: 0.0713; result: 500000500000
Threads: 10; time: 0.0787; result: 500000500000
Threads: 20; time: 0.0807; result: 500000500000
Threads: 50; time: 0.0717; result: 500000500000
Threads: 100; time: 0.0668; result: 500000500000
```

Вывод:
Видим, что результат примерно равен AsyncIO


## Реализация на multiprocessing через значение

В данной реализации для передачи данных между процессами использовалось 
`multiprocessing.Value`

Код:
```python

import multiprocessing
import time
import math


def compute_sum(start, end, res_value):
    sm = sum(range(start, end + 1))
    res_value.acquire()
    res_value.value += sm
    res_value.release()


def compute_with_threading(start, end, n_threads):
    processes = []
    values = []
    step = int(math.ceil((end - start) / n_threads))
    start_i = start
    value = multiprocessing.Value("q", 0)
    while start_i <= end:
        end_i = min(start_i + step, end)

        process = multiprocessing.Process(
            target=compute_sum, args=[start_i, end_i, value]
        )
        process.start()
        processes.append(process)
        start_i = end_i + 1

    for process in processes:
        process.join()

    return value.value


def measure(n_threads):
    start_time = time.perf_counter()
    res = compute_with_threading(1, 1000_000, n_threads)
    elapsed = round(time.perf_counter() - start_time, 4)
    print(f"Processes: {n_threads}; time: {elapsed}; result: {res}")


if __name__ == "__main__":
    n_threads_list = [1, 2, 5, 10]
    for n_threads in n_threads_list:
        measure(n_threads)
```


Результат:
```
Processes: 1; time: 0.2716; result: 500000500000
Processes: 2; time: 0.2046; result: 500000500000
Processes: 5; time: 0.2634; result: 500000500000
Processes: 10; time: 0.4576; result: 500000500000
Processes: 30; time: 0.9976; result: 500000500000
```

Вывод:

Получаем оптимальную картину на 2-5 процессах, а при увеличении скорость падает.
Это связано с тем, что затраты на создание процессов не окупают прирост вычислительной мощности


## Реализация на multiprocessing через очередь

Код:
```python
import multiprocessing
import time
import math


def compute_sum(start, end, queue):
    sm = sum(range(start, end + 1))
    queue.put(sm)


def compute_with_threading(start, end, n_threads):
    processes = []
    step = int(math.ceil((end - start) / n_threads))
    start_i = start
    queue = multiprocessing.Queue()
    while start_i <= end:
        end_i = min(start_i + step, end)
        process = multiprocessing.Process(
            target=compute_sum, args=[start_i, end_i, queue]
        )
        process.start()
        processes.append(process)
        start_i = end_i + 1

    for process in processes:
        process.join()

    result = 0
    while not queue.empty():
        result += queue.get()
    return result


def measure(n_threads):
    start_time = time.perf_counter()
    res = compute_with_threading(1, 1000000, n_threads)
    elapsed = round(time.perf_counter() - start_time, 4)
    print(f"Processes: {n_threads}; time: {elapsed}; result: {res}")


if __name__ == "__main__":

    n_threads_list = [1, 2, 5, 10, 30]
    for n_threads in n_threads_list:
        measure(n_threads)

```

Результат:
```
Processes: 1; time: 0.2835; result: 500000500000
Processes: 2; time: 0.1856; result: 500000500000
Processes: 5; time: 0.2023; result: 500000500000
Processes: 10; time: 0.3622; result: 500000500000
Processes: 30; time: 1.0166; result: 500000500000
```

Вывод:

Работает чуть быстрее, лушче всего работает при 2-5 процессах



## Вывод

AsyncIO и threadin работают примерно с одной скоростью. Multiprocessing работает
чуть медленнее, видимо потому что затраты на создание процессов ниже вычислительной
мощности, которую мы получаем с этого
