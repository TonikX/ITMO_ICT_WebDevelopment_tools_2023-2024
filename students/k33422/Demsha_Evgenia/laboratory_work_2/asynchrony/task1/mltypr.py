import multiprocessing
import time
from task1.naive import calculate_sum
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    num_workers = int(os.getenv('NUM_WORKERS'))
    amount = int(os.getenv('AMOUNT'))
    load = amount // num_workers

    manager = multiprocessing.Manager()
    result_list = manager.list(range(num_workers))
    processes = []

    start_time = time.time()

    for i in range(num_workers):
        process = multiprocessing.Process(target=calculate_sum, args=((strt := i*load), strt + load, result_list, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(sum(result_list))
    print(time.time() - start_time)
