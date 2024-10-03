import time
import threading


def sum_range(l, r, results, ind):
    s = 0
    for i in range(l, r + 1):
        s += i
    results[ind] = s

if __name__ == "__main__":
    n = 4 # Number of threads
    results = [0] * n
    threads = [None] * n

    for i in range(n):
        l = 1 + i * (100_000_000 // n)
        r = (i + 1) * (100_000_000 // n)    
        threads[i] = threading.Thread(target=sum_range, args=[l, r, results, i])

    start = time.time()
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()
        
    total_sum = sum(results)
    finish = time.time()

    print(f"Sum: {total_sum}\nTime: {finish - start}")