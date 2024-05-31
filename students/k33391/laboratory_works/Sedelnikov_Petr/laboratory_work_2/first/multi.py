import multiprocessing
import time


def calculate_sum(start, end):
    return sum(range(start, end))


def worker(start, end, queue):
    queue.put(calculate_sum(start, end))


def main():
    tasks_quantity = 4
    numbers = 1000000
    step = numbers // tasks_quantity
    tasks = []
    queue = multiprocessing.Queue()

    for i in range(tasks_quantity):
        start = i * step + 1
        end = (i + 1) * step + 1
        task = multiprocessing.Process(target=worker, args=(start, end, queue))
        tasks.append(task)
        task.start()

    for task in tasks:
        task.join()

    results = [queue.get() for i in range(tasks_quantity)]
    total = sum(results)
    print(f"Total: {total}")


if __name__ == "__main__":
    print("Multiprocessing")
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
