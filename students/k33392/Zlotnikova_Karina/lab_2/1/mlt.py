import multiprocessing
import time

def calculate_sum(start, end):
    return sum(range(start, end))

def worker(args):
    start, end = args
    return calculate_sum(start, end)

def main():
    tasks_quantity = 4
    numbers = 1000000
    step = numbers // tasks_quantity
    tasks = []
    with multiprocessing.Pool(processes=tasks_quantity) as pool:
        for i in range(tasks_quantity):
            start = i * step + 1
            end = (i + 1) * step + 1
            tasks.append((start, end))
        results = pool.map(worker, tasks)
        total = sum(results)
        print(f"Total: {total}")

if __name__ == "__main__":
    print("Multiprocess")
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")