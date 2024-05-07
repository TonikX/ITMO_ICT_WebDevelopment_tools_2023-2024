from multiprocessing import Pool
from time import time


def calculate_sum(args):
    i_from, i_to = args
    return sum(range(i_from, i_to))


def check_n_splits(n):
    start = time()
    with Pool(n) as p:
        #chunks = np.array_split(range(1, 10**6), n)
        step = 10**6 // n
        chunks = [(i, i + step) for i in range(1, 10**6, step)]
        if chunks[-1][1] != 10**6:
            chunks[-1] = (chunks[-1][0], 10**6)
        result = sum(p.map(calculate_sum, chunks))
    print("Splits:", n)
    print("Result:", result)    
    print("Execution time:", time() - start)
    print()


if __name__ == "__main__":
    for n in range(2, 11):
        check_n_splits(n)