import threading
import time

def calculate_sum(start, end):
    total = 0
    for i in range(start, end+1):
        total += i
    return total

def main():
    start_time = time.time()

    threads = []
    chunk_size = 10_000_000
    num_threads = 4

    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        thread = threading.Thread(target=lambda: print(calculate_sum(start, end)))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
