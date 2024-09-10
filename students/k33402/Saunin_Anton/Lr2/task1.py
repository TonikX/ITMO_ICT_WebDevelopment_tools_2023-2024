import asyncio
import threading
import multiprocessing
import time


async def async_calculate_part(s, e):
    return sum(range(s, e + 1))


async def async_calculate_sum():
    num_tasks = 4
    n = 1000000
    step = n // num_tasks
    tasks = []

    for i in range(num_tasks):
        s = i * step + 1
        e = (i + 1) * step if i != num_tasks - 1 else n
        tasks.append(asyncio.create_task(async_calculate_part(s, e)))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    return total_sum


def mp_calculate_part(s, e, res, idx):
    res[idx] = sum(range(s, e + 1))


def mp_calculate_sum():
    num_tasks = 4
    n = 1000000
    tasks_list = []
    step = n // num_tasks

    manager = multiprocessing.Manager()
    res = manager.list([0] * num_tasks)

    for i in range(num_tasks):
        s = i * step + 1
        e = (i + 1) * step if i != num_tasks - 1 else n
        process = multiprocessing.Process(target=mp_calculate_part, args=(s, e, res, i))
        tasks_list.append(process)
        process.start()

    for process in tasks_list:
        process.join()

    _sum = sum(res)
    return _sum


def thread_calculate_part(s, e, res, idx):
    res[idx] = sum(range(s, e + 1))


def thread_calculate_sum():
    num_tasks = 4
    n = 1000000
    tasks_list = []
    result = [0] * num_tasks
    step = n // num_tasks

    for i in range(num_tasks):
        start = i * step + 1
        end = (i + 1) * step if i != num_tasks - 1 else n
        thread = threading.Thread(target=thread_calculate_part, args=(start, end, result, i))
        tasks_list.append(thread)
        thread.start()

    for thread in tasks_list:
        thread.join()

    total_sum = sum(result)
    return total_sum


if __name__ == '__main__':
    start_time = time.time()
    sum_result = asyncio.run(async_calculate_sum())
    end_time = time.time()
    print(f"Async sum: {sum_result}, Time taken: {end_time - start_time} seconds")

    start_time = time.time()
    sum_result = mp_calculate_sum()
    end_time = time.time()
    print(f"Multiprocessing sum: {sum_result}, Time taken: {end_time - start_time} seconds")


    start_time = time.time()
    sum_result = thread_calculate_sum()
    end_time = time.time()
    print(f"Threading sum: {sum_result}, Time taken: {end_time - start_time} seconds")

