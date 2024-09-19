from multiprocessing import Process, Pool
import time
from common import URLS, parse_and_save


def main(urls):
    num_process = len(urls) if len(urls) < 4 else 4
    pool = Pool(processes=num_process)
    pool.map(parse_and_save, urls)


if __name__ == "__main__":
    start_time = time.time()
    main(URLS)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Mutiprocessing time: {execution_time}")
