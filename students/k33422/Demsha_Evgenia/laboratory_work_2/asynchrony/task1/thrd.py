import threading
import time
from task1.naive import calculate_sum
import os
from dotenv import load_dotenv


if __name__ == '__main__':

    load_dotenv()
    num_workers = int(os.getenv('NUM_WORKERS'))
    amount = int(os.getenv('AMOUNT'))
    load = amount // num_workers

    result_list = [None] * num_workers
    threads = []

    start_time = time.time()

    for i in range(num_workers):
        thread = threading.Thread(target=calculate_sum, args=((strt := i*load), strt + load, result_list, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(sum(result_list))
    print(time.time() - start_time)
