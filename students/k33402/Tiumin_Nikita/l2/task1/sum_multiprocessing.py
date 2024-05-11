import multiprocessing
from time import time

RUNS_NUMBER = 3
CHUNKS_NUMBER = 4
NUMBER = 1000000


def calc(lr):
    l, r = lr
    return sum(range(l, r))


def main():
    args = []

    for i in range(CHUNKS_NUMBER):
        l = int(i * NUMBER / CHUNKS_NUMBER + 1)
        r = int(l + NUMBER / CHUNKS_NUMBER)
        args.append((l, r))

    pool = multiprocessing.Pool(len(args))

    start = time()
    res = pool.map(calc, args)
    pool.close()
    pool.join()
    exec_time = time() - start

    return exec_time, res


if __name__ == "__main__":
    times = []
    for i in range(RUNS_NUMBER):
        next_time, res = main()
        times.append(next_time)
        print(i + 1, ' run: ', next_time, 's. RESULT: ', sum(res))
    print('Average time: ', sum(times) / len(times), 's')


