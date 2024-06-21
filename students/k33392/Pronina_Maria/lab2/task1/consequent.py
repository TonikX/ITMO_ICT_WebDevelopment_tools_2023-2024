import threading
import time


def calculate_sum(start_num, end_num, result):
    res = sum(range(start_num, end_num))
    result.append(res)


def main():
    n = 5
    total = 1000000
    chunk_size = total // n
    result = list()

    for i in range(n):
        start_num = i * chunk_size + 1
        end_num = (i + 1) * chunk_size + 1
        calculate_sum(start_num, end_num, result)

    return sum(result)


if __name__ == "__main__":
    start_time = time.time()
    total_sum = main()
    result_time = time.time() - start_time
    print(f'Sum: {total_sum} \nTime: {result_time}')
