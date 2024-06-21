# Задача 1:

Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных задач для ускорения выполнения.

## Подготовка

Реализуем три различных подхода для сложения чисел в python.

### asyncCode.py

```python
import asyncio
import sys

async def calculate_partial_sum(start, end):
    return sum(range(start, end))

async def calculate_sum_async(num_tasks, total):
    step = total // num_tasks

    tasks = [calculate_partial_sum(i * step + 1, (i + 1) * step + 1) for i in range(num_tasks)]
    results = await asyncio.gather(*tasks)

    return sum(results)

if __name__ == "__main__":
    import time
    num_tasks = int(sys.argv[1])
    total = int(sys.argv[2])
    start_time = time.time()
    result = asyncio.run(calculate_sum_async(num_tasks, total))
    end_time = time.time()
    print(f"Async/await result: {result}, Time taken: {end_time - start_time} seconds")

```

### multiprocessingCode.py

```python
import multiprocessing
import sys

def calculate_partial_sum(start, end):
    return sum(range(start, end))

def calculate_sum_multiprocessing(num_processes, total):
    step = total // num_processes
    pool = multiprocessing.Pool(processes=num_processes)

    tasks = [(i * step + 1, (i + 1) * step + 1) for i in range(num_processes)]
    results = pool.starmap(calculate_partial_sum, tasks)

    return sum(results)

if __name__ == "__main__":
    import time
    num_processes = int(sys.argv[1])
    total = int(sys.argv[2])
    start_time = time.time()
    result = calculate_sum_multiprocessing(num_processes, total)
    end_time = time.time()
    print(f"Multiprocessing result: {result}, Time taken: {end_time - start_time} seconds")
```

### threadingCode.py

```python
import threading
import sys

def calculate_partial_sum(start, end, result, index):
    result[index] = sum(range(start, end))

def calculate_sum_threading(num_threads, total):
    step = total // num_threads
    threads = []
    results = [0] * num_threads

    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step + 1
        thread = threading.Thread(target=calculate_partial_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)

if __name__ == "__main__":
    import time
    num_threads = int(sys.argv[1])
    total = int(sys.argv[2])
    start_time = time.time()
    result = calculate_sum_threading(num_threads, total)
    end_time = time.time()
    print(f"Threading result: {result}, Time taken: {end_time - start_time} seconds")

```

## Тестирование

Подготовим main файл, который будет запускать все 3 различных подхода и выводить результаты. В качестве аргументов дадим возможность указать до какого числа хотим посчитать сумму и сколько потоков / экземпляров должно быть запущено.

### main.py

```python
import subprocess
import pandas as pd
import sys

def run_program(command, num_threads, total):
    result = subprocess.run(command + [str(num_threads), str(total)], capture_output=True, text=True)
    output = result.stdout.strip().split(", ")
    if len(output) < 2:
        print(f"Error in output: {result.stdout}")
        return None, None
    result_value = int(output[0].split(": ")[1])
    time_taken = float(output[1].split(": ")[1].split(" ")[0])
    return result_value, time_taken

def main(num_threads, total):
    methods = {
        "Threading": ["python3", "threadingCode.py"],
        "Multiprocessing": ["python3", "multiprocessingCode.py"],
        "Async/await": ["python3", "asyncCode.py"]
    }

    results = []

    for method, command in methods.items():
        result_value, time_taken = run_program(command, num_threads, total)
        if result_value is not None and time_taken is not None:
            results.append([method, result_value, time_taken])

    df = pd.DataFrame(results, columns=["Method", "Result", "Time Taken (s)"])
    print(df)

if __name__ == "__main__":
    num_threads = int(sys.argv[1])
    total = int(sys.argv[2])
    main(num_threads, total)
```

Протестируем код в режиме 4 экземпляров и 1 млрд для подсчета, получим следующие результаты:

| Method          | Result             | Time Taken (s) |
| --------------- | ------------------ | -------------- |
| Threading       | 500000000500000000 | 8.250351       |
| Multiprocessing | 500000000500000000 | 2.218359       |
| Async/await     | 500000000500000000 | 8.432211       |

Попробуем в режиме 10 экземпляров и 1 млрд для подсчета, получим следующие результаты:

| Method          | Result             | Time Taken (s) |
| --------------- | ------------------ | -------------- |
| Threading       | 500000000500000000 | 8.198584       |
| Multiprocessing | 500000000500000000 | 1.260076       |
| Async/await     | 500000000500000000 | 8.234080       |

## Итоги

При математических задачах направленных на работу с CPU лучше всего себя показывает мультипроцессинг. На втором месте Threading, он показывает результаты хуже примерно в столько раз, во сколько больше потоков было для вычисления у мультипроцессинга и на последнем месте async / await, в данном случае, он не выигрывает для себя время в этой задаче, т.к. она полностью синхронная и по факту ничего не меняется.
