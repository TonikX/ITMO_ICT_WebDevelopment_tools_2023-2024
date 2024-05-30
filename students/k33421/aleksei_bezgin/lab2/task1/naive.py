import time


def calculate_sum(start, end):
    start_time = time.time()
    result = sum(range(start, end))
    print(f"sum from {start} to {end}: {result}")
    print(f"execution time: {round(time.time() - start_time, 5)} seconds")


if __name__ == "__main__":
    calculate_sum(start=0, end=10*10000000)
