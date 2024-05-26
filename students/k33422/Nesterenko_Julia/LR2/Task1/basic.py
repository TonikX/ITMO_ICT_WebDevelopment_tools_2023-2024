from time import time


def calculate_sum(i_from, i_to):
    return sum(range(i_from, i_to))


def calculate_sum_dummy(i_from, i_to):
    s = 0
    for k in range(i_from, i_to):
        s += k
    return s


def calculate_sum_dumb_dummy(i_from, i_to):
    s = 0
    k = i_from
    while k < i_to:
        s += k
        k += 1
    return s


if __name__ == "__main__":
    start = time()
    result = calculate_sum(1, 10**6)
    print("Result:", result)
    print("Execution time:", time() - start)