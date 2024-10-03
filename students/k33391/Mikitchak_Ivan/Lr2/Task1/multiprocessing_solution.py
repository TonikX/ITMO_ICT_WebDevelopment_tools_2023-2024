import time
import multiprocessing


def sum_range(l, r, results):
    s = 0
    for i in range(l, r + 1):
        s += i
    results.put(s)

if __name__ == "__main__":
    n = 4 # Number of processes
    results = multiprocessing.Queue()
    processes = [None] * n

    for i in range(n):
        l = 1 + i * (100_000_000 // n)
        r = (i + 1) * (100_000_000 // n)
        processes[i] = multiprocessing.Process(target=sum_range, args=[l, r, results])

    start = time.time()
    for process in processes:
        process.start()
        
    for process in processes:
        process.join()

    total_sum = 0
    while not results.empty():
        total_sum += results.get()
    finish = time.time()

    print(f"Sum: {total_sum}\nTime: {finish - start}")