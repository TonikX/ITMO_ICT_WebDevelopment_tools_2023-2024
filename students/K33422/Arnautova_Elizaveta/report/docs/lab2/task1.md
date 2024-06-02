**Задача 1. Различия между threading, multiprocessing и async в Python**

**Задача:**  Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных задач для ускорения выполнения.

**Подробности задания:**

- Напишите программу на Python для каждого подхода: threading, multiprocessing и async.
- Каждая программа должна содержать функцию calculate_sum(), которая будет выполнять вычисления.
- Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова async/await и модуль asyncio.
- Каждая программа должна разбить задачу на несколько подзадач и выполнять их параллельно.
Замерьте время выполнения каждой программы и сравните результаты.

**naive**
```python
import time

def calculate_sum(i_from, i_to):
    return sum(range(i_from, i_to))


if __name__ == "__main__":
    times = 10
    av_time = 0
    for i in range (times):
        start_time = time.time()
        result = calculate_sum(1, 1000000)
        end_time = time.time()
        av_time += end_time - start_time

    print(f"Average naive execution time: {av_time / times:.4f} seconds")

```

**threading**
```python
import threading
import time


# Использует генераторное выражение x*x for x in range(start, end) и функцию sum
def calculate_sum(start, end):
    total = sum(x * x for x in range(start, end))
    return total


# Вызывает calculate_sum и сохраняет результат в список results по индексу index
def thread_worker(start, end, results, index):
    results[index] = calculate_sum(start, end)
    # print(results)


def one_thread(num_threads, range_per_thread):
    start_time = time.time()

    for i in range(num_threads):
        start = i * range_per_thread  # вычисляются старт-
        end = (i + 1) * range_per_thread  # финиш для каждого потока
        thread = threading.Thread(target=thread_worker, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)

    end_time = time.time()
    return total_sum, end_time - start_time


if __name__ == "__main__":
    num_threads = 10
    range_per_thread = 10 ** 6 // num_threads
    times = 10
    threads = []
    results = [0] * num_threads

    av_time = 0
    for i in range(times):
        total_sum, timer = one_thread(num_threads, range_per_thread)
        av_time += timer

    print(f"Threading total sum: {total_sum}")
    print(f"Average threading execution time: {av_time / times:.4f} seconds")


```

**multiprocessing**
```python
import multiprocessing
import time


def calculate_sum(start, end):
    total = sum(x * x for x in range(start, end))
    return total


if __name__ == "__main__":
    num_processes = 10
    range_per_process = 10 ** 6 // num_processes
    times = 10

    av_time = 0
    for i in range(times):
        pool = multiprocessing.Pool(processes=num_processes)  # Создаем пул процессов
        # список кортежей с границами диапазонов
        tasks = [(i * range_per_process, (i + 1) * range_per_process) for i in range(num_processes)]

        start_time = time.time()
        results = pool.starmap(calculate_sum, tasks)
        pool.close()
        pool.join()

        total_sum = sum(results)
        end_time = time.time()

        av_time = av_time + end_time - start_time

    print(f"Multiprocessing total sum: {total_sum}")
    print(f"Multiprocessing execution time: {av_time / times:.4f} seconds")

```

**asyncio**
```python
import asyncio
import time


async def calculate_sum(start, end):
    total = sum(x * x for x in range(start, end))
    return total


async def main():
    num_tasks = 10
    range_per_task = 10 ** 6 // num_tasks
    times = 10

    av_time = 0
    for i in range(times):
        tasks = [calculate_sum(i * range_per_task, (i + 1) * range_per_task) for i in range(num_tasks)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_sum = sum(results)
        end_time = time.time()

        av_time = av_time + end_time - start_time

    print(f"Asyncio total sum: {total_sum}")
    print(f"Asyncio execution time: {av_time/times:.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main())

```

Во всех примерах код выполнялся 10 раз, все делилось на 10 процессов/потоков/запросов для всех вычислялось среднее арифметическое времени выполнения.

<table>
  <thead>
    <tr>
      <th></th>
      <th>Naive</th>
      <th>Threading</th>
      <th>Multiprocessing</th>
      <th>Asyncio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Average</th>
      <td>0.0151</td>
      <td>0.0632</td>
      <td>0.1009</td>
      <td>0.0640</td>
    </tr>
    <tr>
      <th>Max</th>
      <td>0.0159</td>
      <td>0.0989</td>
      <td>0.1294</td>
      <td>0.0698</td>
    </tr>
    <tr>
      <th>Min</th>
      <td>0.0139</td>
      <td>0.0583</td>
      <td>0.0619</td>
      <td>0.0648</td>
    </tr>
  </tbody>
</table>

И тут, как можно увидеть, происходит веселое: наивный алгоритм отрабатывает ощутимо быстрее, чем что бы то ни было (даже если уменьшать количество процессов/потоков/запросов). Потому что на то, чтоб просто сотворить это все, тоже уходит время... и в рамках выполнения этой задачи это время критично.