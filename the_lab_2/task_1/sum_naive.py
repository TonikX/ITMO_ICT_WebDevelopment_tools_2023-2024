import time


def calculate_sum(i_from, i_to):
    return sum(range(i_from, i_to))


if __name__ == "__main__":
    start_time = time.time()
    print(calculate_sum(1, 1000000))
    print(f"Naive time: {time.time() - start_time}")
