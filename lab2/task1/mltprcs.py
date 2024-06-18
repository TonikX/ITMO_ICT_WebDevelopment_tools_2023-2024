from multiprocessing import Pool
from time import time


def calculate_sum(args):
    i_from, i_to = args
    return sum(range(i_from, i_to))


if __name__ == "__main__":
    start = time()
    n = 4
    with Pool(n) as p:
        step = 10**6 // n
        chunks = [(i, i + step) for i in range(1, 10**6, step)]
        if chunks[-1][1] != 10**6:
            chunks[-1] = (chunks[-1][0], 10**6)
        RESULT = sum(p.map(calculate_sum, chunks))

    print("Result:", RESULT)
    print("Execution time:", time() - start)
