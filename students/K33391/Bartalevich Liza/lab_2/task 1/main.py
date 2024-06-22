from threading import Thread
from multiprocessing import Pool
import asyncio


def thr_calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.append(total)


def thread_main():
    result = []
    threads = []
    chunk_size = 10**5

    for i in range(0, 10**6, chunk_size):
        t = Thread(target=thr_calculate_sum, args=(i+1, i+chunk_size+1, result))

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Result of sum:", sum(result))



def mpl_calculate_sum(start, end):
    total = sum(range(start, end))
    return total


def multyproc_main():
    chunk_size = 10**5

    pool = Pool(processes=10**6 // chunk_size)
    result = [pool.apply(mpl_calculate_sum, (i+1, i+chunk_size+1)) for i in range(0, 10**6, chunk_size)]

    print("Result of sum:", sum(result))


async def async_calculate_sum(start, end):
    total = sum(range(start, end))
    return total


async def async_main():
    tasks = []
    chunk_size = 10**5

    for i in range(0, 10**6, chunk_size):
        task = asyncio.create_task(async_calculate_sum(i+1, i+chunk_size+1))
        tasks.append(task)

    result = await asyncio.gather(*tasks)

    print("Result of sum:", sum(result))


if __name__ == '__main__':
    thread_main()
    multyproc_main()
    asyncio.run(async_main())