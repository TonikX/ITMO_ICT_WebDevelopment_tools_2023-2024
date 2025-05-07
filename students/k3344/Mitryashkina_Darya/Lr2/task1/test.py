import time

def calculate_sum(start, end):
    print(f"Calculating: start {start}, end {end}")
    total = 0
    for i in range(start, end):
        total += i
    return total

def main():
    N = 10**9
    num_threads = 10
    results = [0] * num_threads

    for i in range(num_threads):
        start = i * N // num_threads
        end = (i + 1) * N // num_threads
        results.append(calculate_sum(start, end))  

    total_sum = sum(results) + N
    print("Total sum:", total_sum)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")

# Total sum: 500000000500000000
# Time taken: 48.17 seconds