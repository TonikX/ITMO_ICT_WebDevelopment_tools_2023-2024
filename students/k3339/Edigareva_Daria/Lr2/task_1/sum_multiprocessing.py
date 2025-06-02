import time
import multiprocessing as mp

N = 1_000_000_000
NUM_PROCS = 4

def partial_sum_range(start: int, end: int) -> int:
    total = 0
    for i in range(start, end + 1):
        total += i
    print(f"Process finished range {start}-{end}")
    return total

if __name__ == "__main__":
    chunk_size = N // NUM_PROCS
    ranges = []
    for i in range(NUM_PROCS):
        start = i * chunk_size + 1
        end = N if i == NUM_PROCS - 1 else (i + 1) * chunk_size
        ranges.append((start, end))
    start_time = time.time()

    with mp.Pool(processes=NUM_PROCS) as pool:
        results = pool.starmap(partial_sum_range, ranges)
    total_sum = sum(results)
    elapsed = time.time() - start_time
    print(f"Total sum = {total_sum}")
    print(f"Completed in {elapsed:.2f} seconds")
