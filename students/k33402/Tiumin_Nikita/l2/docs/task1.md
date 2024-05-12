# Задание 1

С помощью трех подходов: threading, multiprocessing и async/await
сумма чисел от 1 до 1000000 была разбита на заранее задданное число чанков и вычислена


## sum_threading.py

```python
from multiprocessing.pool import ThreadPool
from time import time

RUNS_NUMBER = 3
CHUNKS_NUMBER = 4
NUMBER = 1000000


def calc(lr):
    l, r = lr
    return sum(range(l, r))


def main():
    args = []

    for i in range(CHUNKS_NUMBER):
        l = int(i * NUMBER / CHUNKS_NUMBER + 1)
        r = int(l + NUMBER / CHUNKS_NUMBER)
        args.append((l, r))

    pool = ThreadPool(len(args))

    start = time()
    res = pool.map(calc, args)
    pool.close()
    pool.join()
    exec_time = time() - start

    return exec_time, res


if __name__ == "__main__":
    times = []
    for i in range(RUNS_NUMBER):
        next_time, res = main()
        times.append(next_time)
        print(i + 1, ' run: ', next_time, 's. RESULT: ', sum(res))
    print('Average time: ', sum(times) / len(times), 's')
```

## multiprocessing_sum.py

```python
 import multiprocessing
from time import time

RUNS_NUMBER = 3
CHUNKS_NUMBER = 4
NUMBER = 1000000


def calc(lr):
    l, r = lr
    return sum(range(l, r))


def main():
    args = []

    for i in range(CHUNKS_NUMBER):
        l = int(i * NUMBER / CHUNKS_NUMBER + 1)
        r = int(l + NUMBER / CHUNKS_NUMBER)
        args.append((l, r))

    pool = multiprocessing.Pool(len(args))

    start = time()
    res = pool.map(calc, args)
    pool.close()
    pool.join()
    exec_time = time() - start

    return exec_time, res


if __name__ == "__main__":
    times = []
    for i in range(RUNS_NUMBER):
        next_time, res = main()
        times.append(next_time)
        print(i + 1, ' run: ', next_time, 's. RESULT: ', sum(res))
    print('Average time: ', sum(times) / len(times), 's')
```

## asyncio_sum.py

```python
import asyncio
from time import time

RUNS_NUMBER = 3
CHUNKS_NUMBER = 4
NUMBER = 1000000


async def calc(l, r):
    return sum(range(l, r))


async def main():
    tasks = []

    for i in range(CHUNKS_NUMBER):
        l = int(i * NUMBER / CHUNKS_NUMBER + 1)
        r = int(l + NUMBER / CHUNKS_NUMBER)

        task = asyncio.create_task(calc(l, r))
        tasks.append(task)

    start = time()
    res = await asyncio.gather(*tasks)
    exec_time = time() - start

    return exec_time, res


if __name__ == "__main__":
    times = []
    for i in range(RUNS_NUMBER):
        next_time, res = asyncio.run(main())
        times.append(next_time)
        print(i + 1, ' run: ', next_time, 's. RESULT: ', sum(res))
    print('Average time: ', sum(times) / len(times), 's')
```

## Выводы

|             | **Threading** | **Multiprocessing** | **Asyncio** |
| ----------- |---------------| ----------------- |-------------|
| 1           | 0.029         | 0.16           | 0.027       |
| 2           | 0.030         | 0.14           | 0.028       |
| 3           | 0.029         | 0.12           | 0.027       |
| **Avg**     | 0.029         | 0.14           | 0.0273      |

- **Threading**: Время выполнения одного порядка с asyncio. Однако, Threading ограничен GIL, что может замедлить выполнение на многопроцессорных системах.
- **Multiprocessing**: Проигрывает на порядок остальным методам. Скорее всего время увеличено из-за ресурсных затрат на переключчение между процессами.
- **Asyncio**:  Обеспечивает лучшую производительность благодаря эффективному использованию асинхронных операций без создания дополнительных процессов или потоков.


## Приложение


|             | **Threading** | **Multiprocessing** | **Asyncio** |
| ----------- |---------------| ---------------- |-------------|
| 1           | 28.88         | 11.23          | 28.44       |
| 2           | 28.90         | 10.67          | 29.03       |
| 3           | 29.68         | 10.90          | 34.16       |
| **Avg**     | 29.15         | 10.93          | 30.54       |

На 1 000 000 000 multiprocessing показал наилучший результат. Отсюда можно сделать вывод, что с ростом сложности вычислений затраты на создание и управление процессами нивелируется.