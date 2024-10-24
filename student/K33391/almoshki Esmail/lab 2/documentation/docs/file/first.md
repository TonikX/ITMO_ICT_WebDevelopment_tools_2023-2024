# Python Parallelism Example: Async, Multiprocessing, and Multithreading

This document contains examples of how to perform parallel computations using three different approaches in Python:
- Asynchronous programming (`asyncio`)
- Multiprocessing
- Multithreading

## async.py

This script demonstrates how to use asynchronous programming (`asyncio`) to calculate the sum of numbers in different ranges concurrently.

### Code:

```python
import asyncio
from time import time

async def calculate_sum(start: int, end:int) -> int:
    '''
    Function to calculate the sum of integer numbers falling between the range [a,b]

    Parameters
    -----
    start - the start of the interval
    end - the end of the interval
    '''
    sum = 0
    for i in range(start, end + 1):
        sum += i
    return sum

async def main():
    start_time = time()
    tasks = []
    for i in range(4):
        task = asyncio.create_task(calculate_sum(i * 250000, (i + 1) * 250000))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    print(f'time: {time() - start_time}')
    print(sum(results))

if __name__ == "__main__":
    asyncio.run(main())
```
## Explanation:
  - ### calculate_sum():
   An asynchronous function that calculates the sum of numbers between a given range.


## multiprocess.py
This script demonstrates how to use the multiprocessing module to split the computation of the sum of integers into multiple processes.


### Code:
```python
import multiprocessing
from time import time

def calculate_sum(start: int, end: int, arr) -> int:
    '''
    Function to calculate the sum of integer numbers falling between the range [a,b]

    Parameters
    -----
    start - the start of the interval
    end - the end of the interval
    '''
    sum = 0
    for i in range(start, end + 1):
        sum += i
    arr.append(sum)
    return sum

def main():
    processes = []
    nums = multiprocessing.Manager().list()
    start_time = time()

    for i in range(0, 4):
        process = multiprocessing.Process(target=calculate_sum, args=((250000 * i) + 1, 250000 * (i + 1), nums))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    
    print(f'time: {time() - start_time}')
    print(sum(nums))

if __name__ == "__main__":
    main()
```
## Explanation:
### calculate_sum():
 Function that computes the sum of integers in the specified range and appends the result to a shared list.


## multithreading.py
This script demonstrates how to use the threading module to perform the same calculation using multiple threads.

### Code:
```python
import threading
from time import time 
import numpy as np

def calculate_sum(start: int, end: int, arr:np.ndarray) -> int:
    '''
    Function to calculate the sum of integer numbers falling between the range [a,b]

    Parameters
    -----
    start - the start of the interval
    end - the end of the interval
    '''
    sum = 0
    for i in range(start, end + 1):
        sum += i
    arr.append(sum)
    return sum

threads = []
sums = []
start_time = time()

for i in range(0, 4):
    thread = threading.Thread(target=calculate_sum, args=((250000 * i) + 1, 250000 * (i + 1), sums))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f'time: {time() - start_time}')
print(sum(sums))
```

## Explanation:
### calculate_sum(): 
A function that calculates the sum of integers in a range and appends the result to a shared list.
Threads: The script creates 4 threads to compute the sums concurrently, then joins the threads and prints the total time and result.

