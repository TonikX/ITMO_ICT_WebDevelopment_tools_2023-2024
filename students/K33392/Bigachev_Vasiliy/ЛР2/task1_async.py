import asyncio
from time import time, sleep

first_number = 1
last_number = 1000000

NUMBER_OF_THREADS = 4
NUMBERS_FOR_THREADS = last_number // NUMBER_OF_THREADS

results = [0] * NUMBER_OF_THREADS 

# Возвращает сумму чисел от start до end включительно
async def calculate_sum_async(i: int, start: int, end: int):
    #await asyncio.sleep(1)
    results[i] = sum(range(start, end+1))

def calculate_sum_non_async(start: int, end: int):
    #sleep(1)
    return sum(range(start, end+1))
    
# Основной поток
async def asyncio_calculate_sum():
    threads = []

    for i in range(NUMBER_OF_THREADS):
        poll_task = asyncio.create_task(calculate_sum_async(i, NUMBERS_FOR_THREADS * i + 1, NUMBERS_FOR_THREADS * (i + 1)))
        threads.append(poll_task)

    await asyncio.gather(*threads)
    
    print("Result(asyncio): " + str(sum(results)))

def non_asyncio_calculate_sum():
    calculate_sum_non_async(first_number, last_number)
    print("Result(non asyncio): " + str(sum(results)))

n_tests = 10

times = []
for i in range(n_tests):
    start = time()
    asyncio.run(asyncio_calculate_sum())
    end = time()
    times.append(end-start)
result_avg_time = sum(times)/n_tests
print("AVG time: " + str(result_avg_time))

times = []
for i in range(n_tests):
    start = time()
    non_asyncio_calculate_sum()
    end = time()
    times.append(end-start)
result_avg_time = sum(times)/n_tests
print("AVG time: " + str(result_avg_time))