import threading

def calculate_sum(start, end):
    total = 0
    for i in range(start, end):
        total += i
    return total

def main():
    num_threads = 4
    chunk_size = 1000000 // num_threads
    threads = []
    results = []

    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1
        thread = threading.Thread(target=lambda: results.append(calculate_sum(start, end)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_result = sum(results)
    print(final_result)

if __name__ == "__main__":
    import time

    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")