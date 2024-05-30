import time


def calculate_sum(start, end):
    partial_sum = sum(range(start, end))
    return partial_sum


def main():
    total_sum = calculate_sum(1, 1000001)
    print("Total sum without parallelization:", total_sum)


if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time = time.time() - start_time
    print("Elapsed time:", elapsed_time)
