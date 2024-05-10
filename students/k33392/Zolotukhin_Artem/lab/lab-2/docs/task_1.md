# Задача 1

Каждый из подходов используется для решения задачи суммирования всех чисел от 1 до 1000000, разбивая вычисления на несколько параллельных задач для ускорения выполнения.

## Threading

```python
import threading
from util import get_function_execution_time_sec


def calculate_sum(start, end, container: list):
    total = 0
    for num in range(start, end + 1):
        total += num

    container.append(total)


def main():
    num_threads = 4
    start = 1
    end = 1000000
    step = int(end / num_threads)

    threads = []
    container = []
    for i in range(num_threads):
        thread = threading.Thread(target=calculate_sum, args=(start + i * step, start + (i + 1) * step - 1, container))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Сумма чисел от 1 до 1000000: {sum(container)}")


if __name__ == "__main__":
    time_sec, *_ = get_function_execution_time_sec(main)
    print(f"Затраченное время - {time_sec:.3f} сек")
```

Затраченное время - 0.067 сек

## Multiprocessing

```python
import multiprocessing
from util import get_function_execution_time_sec


def calculate_sum(start, end, container: multiprocessing.Queue):
    total = 0
    for num in range(start, end + 1):
        total += num

    container.put(total)


def main():
    num_processes = 4
    start = 1
    end = 1000000
    step = int(end / num_processes)

    processes = []
    queue = multiprocessing.Queue()
    for i in range(num_processes):
        process = multiprocessing.Process(target=calculate_sum, args=(start + i * step, start + (i + 1) * step - 1, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Сумма чисел от 1 до 1000000: {sum(queue.get() for _ in range(num_processes))}")


if __name__ == "__main__":
    time_sec, *_ = get_function_execution_time_sec(main)
    print(f"Затраченное время - {time_sec:.3f} сек")
```

Затраченное время - 0.252 сек

## Async \ Await

```python
import asyncio
from util import get_function_execution_time_sec_async


async def calculate_sum(start, end):
    total = 0
    for num in range(start, end + 1):
        total += num
    return total


async def main():
    num_tasks = 4
    start = 1
    end = 1000000
    step = int(end / num_tasks)

    tasks = []
    for i in range(num_tasks):
        task = asyncio.create_task(calculate_sum(start + i * step, start + (i + 1) * step - 1))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)

    print(f"Сумма чисел от 1 до 1000000: {total_sum}")


async def wrapper():
    time_sec, *_ = await get_function_execution_time_sec_async(main)
    print(f"Затраченное время - {time_sec:.3f} сек")


if __name__ == "__main__":
    asyncio.run(wrapper())
```

Затраченное время - 0.055 сек

## Выводы

| Method\Time | Threading | Multiprocessing | Async/Await |
| ----------- | --------- | --------------- | ----------- |
| 1           | 0.063     | 0.263           | 0.053       |
| 2           | 0.065     | 0.284           | 0.064       |
| 3           | 0.063     | 0.266           | 0.058       |
| Avg         | 0.064     | 0.271           | 0.058       |

Можем видеть, что самыми эффективными подходами оказались threading и async\await, обходя обход multiprocessing +- в 5 раз.
Данный результат может быть связан с что связано с дополнительными затратами на создание и управление процессами.
