# from task1.workers.async_worker import AsyncWorker
# from task1.workers.sync_worker import SyncWorker
import time

from task1.async_worker import AsyncWorker
from task1.multiprocess_worker import MultiprocessWorker
from task1.threading_worker import ThreadingWorker


def main():
    start = 0
    end = 400_000_000
    n_tasks = 8

    workers = [
        AsyncWorker(start, end, n_tasks),
        ThreadingWorker(start, end, n_tasks),
        MultiprocessWorker(start, end, n_tasks)
    ]

    for worker in workers:
        start_time = time.time()
        result = worker.run()
        end_time = time.time()
        print(worker.__class__.__name__, end_time - start_time, result)


if __name__ == '__main__':
    main()
