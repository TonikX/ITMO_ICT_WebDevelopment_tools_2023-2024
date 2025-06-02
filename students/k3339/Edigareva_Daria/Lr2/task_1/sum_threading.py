import threading
import time

N = 1_000_000_000
NUM_THREADS = 4

partial_sums = [0 for _ in range(NUM_THREADS)]

def partial_sum(start: int, end: int, index: int):
    total = 0
    for i in range(start, end + 1):
        total += i
    partial_sums[index] = total
    thread_name = threading.current_thread().name
    print(f"Thread {thread_name} finished calculating its sum.")

if __name__ == "__main__":
    chunk_size = N // NUM_THREADS
    threads = []
    start_time = time.time()
    for i in range(NUM_THREADS):
        start = i * chunk_size + 1
        end = N if i == NUM_THREADS - 1 else (i + 1) * chunk_size
        t = threading.Thread(target=partial_sum, args=(start, end, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    total_sum = sum(partial_sums)
    elapsed = time.time() - start_time
    print(f"Total sum = {total_sum}")
    print(f"Completed in {elapsed:.2f} seconds")
