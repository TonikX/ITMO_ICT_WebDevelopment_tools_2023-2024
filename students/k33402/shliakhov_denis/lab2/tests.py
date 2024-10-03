import asyncio
import threading
import multiprocessing
import time

async def partial_sum_async(start, end):
    return sum(range(start, end))

def partial_sum_thread(start, end, results, index):
    total = sum(range(start, end))
    results[index] = total

def partial_sum_multiprocess(start, end):
    return sum(range(start, end))

async def calculate_sum_with_asyncio(n):
    num_tasks = 4
    step = n // num_tasks
    tasks = [partial_sum_async(i * step + 1, (i + 1) * step + 1 if i < num_tasks - 1 else n + 1) for i in range(num_tasks)]

    results = await asyncio.gather(*tasks)

    return sum(results)

def calculate_sum_with_threading(n):
    num_threads = 4
    threads = []
    results = [0] * num_threads
    step = n // num_threads

    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step + 1 if i < num_threads - 1 else n + 1
        thread = threading.Thread(target=partial_sum_thread, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)

def calculate_sum_with_multiprocessing(n):
    num_processes = 4
    pool = multiprocessing.Pool(processes=num_processes)
    step = n // num_processes
    tasks = [(i * step + 1, (i + 1) * step + 1 if i < num_processes - 1 else n + 1) for i in range(num_processes)]

    results = pool.starmap(partial_sum_multiprocess, tasks)
    pool.close()
    pool.join()

    return sum(results)

if __name__ == '__main__':
    n = 1000000
    start_time = time.time()
    result = calculate_sum_with_multiprocessing(n)
    end_time = time.time()

    print(f"Multiprocessing Result: {result}, Time: {end_time - start_time} seconds")

    start_time = time.time()
    result = asyncio.run(calculate_sum_with_asyncio(n))
    end_time = time.time()

    print(f"Asyncio Result: {result}, Time: {end_time - start_time} seconds")

    start_time = time.time()
    result = calculate_sum_with_threading(n)
    end_time = time.time()

    print(f"Threading Result: {result}, Time: {end_time - start_time} seconds")
