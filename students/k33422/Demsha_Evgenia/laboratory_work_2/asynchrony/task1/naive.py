import time
from dotenv import load_dotenv
import os


def calculate_sum(start, end, results, res_id):
    curr_sum = 0
    for num in range(start, end + 1):
        curr_sum += num
    print(f'task {res_id}, result {curr_sum}')
    results[res_id] = curr_sum


if __name__ == '__main__':
    load_dotenv()
    amount = int(os.getenv('AMOUNT'))
    result_list = [None]

    start_time = time.time()

    calculate_sum(0, amount, result_list, 0)
    print(sum(result_list))
    print(time.time() - start_time)
