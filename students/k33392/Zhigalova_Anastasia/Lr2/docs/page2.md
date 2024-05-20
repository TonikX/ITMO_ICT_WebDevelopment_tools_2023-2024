# Код ч.1

## asyncio

```
import asyncio
from time import time

async def calculate_sum(start, end):
    return sum(range(start, end + 1))

async def main():
    tasks = []
    num_tasks = 10
    total_numbers = 1000000
    chunk_size = total_numbers // num_tasks
    start_time = time()

    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_tasks - 1 else total_numbers
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    
    print(f"Total Sum: {total_sum}")
    print(f"Time taken: {time() - start_time}")

if __name__ == "__main__":
    asyncio.run(main())
```


## multiprocessing

```
import multiprocessing
from time import time

def calculate_sum(start, end, result, index):
    total = sum(range(start, end + 1))
    result[index] = total

def main():
    processes = []
    num_processes = 10
    manager = multiprocessing.Manager()
    result = manager.list([0] * num_processes)
    total_numbers = 1000000
    chunk_size = total_numbers // num_processes
    start_time = time()

    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_processes - 1 else total_numbers
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, result, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = sum(result)
    print(f"Total Sum: {total_sum}")
    print(f"Time taken: {time() - start_time}")

if __name__ == "__main__":
    main()
```



## threading

```
import threading
from time import time

def calculate_sum(start, end, result, index):
    total = sum(range(start, end + 1))
    result[index] = total

def main():
    threads = []
    num_threads = 10
    result = [0] * num_threads
    total_numbers = 1000000
    chunk_size = total_numbers // num_threads
    start_time = time()

    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_threads - 1 else total_numbers
        thread = threading.Thread(target=calculate_sum, args=(start, end, result, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print(f"Total Sum: {total_sum}")
    print(f"Time taken: {time() - start_time}")

if __name__ == "__main__":
    main()
```