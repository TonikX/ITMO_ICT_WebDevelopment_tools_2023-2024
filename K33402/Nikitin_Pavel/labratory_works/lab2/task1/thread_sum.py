import threading

TOTAL = 1000000
NUM_THREADS = 10

def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end+1))
    result.append(partial_sum)

def main():
    threads = []
    result = []

    for i in range(NUM_THREADS):
        start = i * (TOTAL // NUM_THREADS) + 1
        end = (i + 1) * (TOTAL // NUM_THREADS)
        thread = threading.Thread(target=calculate_sum, args=(start, end, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print("Total sum using threading:", total_sum)

if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print("Execution time:", time.time() - start_time)
