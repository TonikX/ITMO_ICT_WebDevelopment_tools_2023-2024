# Первое задание

| approach        | mean time +- std (sec) |
|-----------------|----------------------|
| naive           | 1.33 +- 0.02         |
| threading       | 1.37 +- 0.03         |
| multiprocessing | 	0.44 +- 0.01        |
| asyncio         |     1.33 +- 0.01     |

Тут с заметным успехом всех обыгрывает multiprocessing.
Threading находится на уровне naive из-за CPU/bound операций и тратами на context switching.
Причины провала asyncio мне неизвестны.

# Сниппеты кода

1. Наивная реализация
```commandline
def calculate_sum(start, end):
    start_time = time.time()
    result = sum(range(start, end))
    print(f"sum from {start} to {end}: {result}")
    print(f"execution time: {round(time.time() - start_time, 5)} seconds")
```

2. multithreading
```commandline
def calculate_sum(start, end):
    result = sum(range(start, end))
    print(f"sum from {start} to {end}: {result}")

def main(num_of_tasks=5, step=1000000):
    start_time = time.time()
    threads = []
    for i in range(num_of_tasks):
        t = threading.Thread(target=calculate_sum, args=(i*step+1, (i+1)*step))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"execution time: {round(time.time() - start_time, 5)} seconds")
```

3. multiprocessing
```commandline
def calculate_sum(start, end):
    result = sum(range(start, end))
    print(f"sum from {start} to {end}: {result}")

def main(num_of_tasks=5, step=1000000):
    start_time = time.time()
    processes = []
    for i in range(num_of_tasks):
        p = multiprocessing.Process(target=calculate_sum, args=(i*step+1, (i+1)*step))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"execution time: {round(time.time() - start_time, 5)} seconds")
```

4. asyncio
```commandline
async def calculate_sum(start, end):
    result = sum(range(start, end))
    print(f"sum from {start} to {end}: {result}")

async def main(num_of_tasks=5, step=1000000):
    start_time = time.time()
    tasks = []
    for i in range(num_of_tasks):
        task = asyncio.create_task(calculate_sum(i*step+1, (i+1)*step))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    print(f"execution time: {round(time.time() - start_time, 5)} seconds")
```