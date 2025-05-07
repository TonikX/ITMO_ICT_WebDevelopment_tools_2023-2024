import multiprocessing
import time

def calculate_sum(args):
    start, end = args
    print(f"Calculating: start {start}, end {end}")
    total = 0
    for i in range(start, end):
        total += i
    return total

def main():
    N = 10**12
    num_processes = multiprocessing.cpu_count()
    print(f"Using {num_processes} processes")

    chunk_size = N // num_processes
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]

    if ranges[-1][1] < N:
        ranges[-1] = (ranges[-1][0], N)

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(calculate_sum, ranges)

    total_sum = sum(results) + N
    print("Total sum:", total_sum)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")

# N = 10**9
# Total sum: 500000000500000000
# Time taken: 18.98 seconds

# N = 10**12
# 