import multiprocessing
import time


def calculate_sum(start, end):
    return sum(range(start, end))

def worker(start, end, queue):
    queue.put(calculate_sum(start, end))

if __name__ == '__main__':
    print("Multiprocessing")
    start_time = time.time()

    tasks = 7
    total = 1000000
    step = total // tasks
    tasks_arr = []
    queue = multiprocessing.Queue()

    start = 1
    end = step + total % tasks + 1

    for i in range(tasks):
        task = multiprocessing.Process(target=worker, args=(start, end, queue))
        start = end
        end = end + step
        tasks_arr.append(task)
        task.start()

    for task in tasks_arr:
        task.join()

    results = [queue.get() for i in tasks_arr]
    total_sum = sum(results)
    print(f"Total: {total_sum}")

    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
    print("Гаусс справился бы быстрее")