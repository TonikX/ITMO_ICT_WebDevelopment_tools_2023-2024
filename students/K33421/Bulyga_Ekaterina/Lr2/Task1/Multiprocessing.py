import multiprocessing
import time


def calculate_sum(args):
    start, stop = args
    summary = 0
    for i in range(start, stop):
        summary += i
    return summary


def main():
    pool = multiprocessing.Pool()

    results = pool.map(calculate_sum, [(i, i + 10**4) for i in range(1, 10**9, 10**4)])

    pool.close()
    pool.join()

    return sum(results)


if __name__ == '__main__':
    time_start = time.time()
    print(main())
    print(time.time() - time_start)
# Время выполнения: 0.29891276359558105
# Время выполнения: 6.393806457519531
