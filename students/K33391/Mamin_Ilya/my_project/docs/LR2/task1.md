# Задача 1. Различия между threading, multiprocessing и async в Python

**Задача: Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных задач для ускорения выполнения.**

**Подробности задания:**

- Напишите программу на Python для каждого подхода: threading, multiprocessing и async.
- Каждая программа должна содержать функцию calculate_sum(), которая будет выполнять вычисления.
- Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова async/await и модуль asyncio.
- Каждая программа должна разбить задачу на несколько подзадач и выполнять их параллельно.
- Замерьте время выполнения каждой программы и сравните результаты.

## Решение:

### asynic.py

```python
import asyncio
from time import time


async def calculate_sum(args):
    global RESULT
    i_from, i_to = args
    s = sum(range(i_from, i_to))
    RESULT += s


async def main(n):
    step = 10**6 // n
    chunks = [(i, i + step) for i in range(1, 10**6, step)]
    if chunks[-1][1] != 10**6:
        chunks[-1] = (chunks[-1][0], 10**6)

    async with asyncio.TaskGroup() as tg:
        for chunk in chunks:
            tg.create_task(calculate_sum(chunk))


if __name__ == "__main__":
    start = time()
    RESULT = 0
    asyncio.run(main(4))
    print("Result:", RESULT, "Execution time:", time() - start)

```

```
Result: 499999500000
Execution time: 0.07601785659790039
```

### mltprcs.py

```python
from multiprocessing import Pool
from time import time


def calculate_sum(args):
    i_from, i_to = args
    return sum(range(i_from, i_to))


if __name__ == "__main__":
    start = time()
    n = 4
    with Pool(n) as p:
        step = 10**6 // n
        chunks = [(i, i + step) for i in range(1, 10**6, step)]
        if chunks[-1][1] != 10**6:
            chunks[-1] = (chunks[-1][0], 10**6)
        RESULT = sum(p.map(calculate_sum, chunks))

    print("Result:", RESULT)
    print("Execution time:", time() - start)
```

```
Result: 499999500000
Execution time: 0.688213586807251
```

### thrd.py

```python
import threading
from time import time

lock = threading.Lock()


def calculate_sum(i_from, i_to):
    global RESULT
    lock.acquire()
    RESULT += sum(range(i_from, i_to))
    lock.release()


if __name__ == "__main__":
    start = time()
    n = 4
    RESULT = 0
    step = 10**6 // n
    chunks = [(i, i + step) for i in range(1, 10**6, step)]
    if chunks[-1][1] != 10**6:
        chunks[-1] = (chunks[-1][0], 10**6)

    threads = [threading.Thread(target=calculate_sum, args=chunk) for chunk in chunks]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Result:", RESULT)
    print("Execution time:", time() - start)
```

```
Result: 499999500000
Execution time: 0.07540440559387207
```
