import multiprocessing
import time

THREADS_COUNT = 20
COUNT = 10_000_000


def cpu_bound_time(_):
    time.sleep(0.3)
    res = sum((x for x in range(COUNT)))
    return res


def cpu_bound(lock):
    lock.acquire()
    res = sum((x for x in range(COUNT)))
    lock.release()
    return res


# def main():
#     with multiprocessing.Manager() as manager:
#         lock = manager.Lock()
#         with multiprocessing.Pool(processes=THREADS_COUNT) as pool:
#             results = pool.map(cpu_bound_time, [_ for _ in range(THREADS_COUNT)])
#             # results = pool.map(cpu_bound, [lock for _ in range(THREADS_COUNT)])
#             return sum(results)


def main():
    with multiprocessing.Pool(processes=THREADS_COUNT) as pool:
        results = pool.map(cpu_bound_time, range(THREADS_COUNT))
        return sum(results)


if __name__ == "__main__":
    main()
