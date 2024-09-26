import time
import threading
import multiprocessing
import asyncio

NUM_TASKS = 4
NUMBERS = 1000000


def calculate_sum(start, end):
    total = 0
    for i in range(start, end + 1):
        total += i
    return total


def threading_example():
    threads = []
    chunk_size = NUMBERS // NUM_TASKS

    start_time = time.time()
    for i in range(NUM_TASKS):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        thread = threading.Thread(target=calculate_sum, args=(start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threading time: {end_time - start_time:.4f} seconds")


def multiprocessing_example():
    processes = []
    chunk_size = NUMBERS // NUM_TASKS

    start_time = time.time()
    for i in range(NUM_TASKS):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        process = multiprocessing.Process(target=calculate_sum, args=(start, end))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Multiprocessing time: {end_time - start_time:.4f} seconds")


async def async_calculate_sum(start, end):
    return calculate_sum(start, end)

async def asyncio_example():
    tasks = []
    chunk_size = NUMBERS // NUM_TASKS

    start_time = time.time()
    for i in range(NUM_TASKS):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        task = asyncio.create_task(async_calculate_sum(start, end))
        tasks.append(task)

    await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Asyncio time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    threading_example()
    multiprocessing_example()
    asyncio.run(asyncio_example())
