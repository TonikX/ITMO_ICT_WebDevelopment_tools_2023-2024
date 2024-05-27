from time import time


def log_time(func, *args):
    start = time()
    func(*args)
    print('Exec time: ', time() - start)


async def log_time_async(func, *args):
    start = time()
    await func(*args)
    print('Exec time: ', time() - start)