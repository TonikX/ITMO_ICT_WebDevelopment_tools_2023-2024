import threading
from time import time

def calculate_sum(start, end, result, index):
    total = sum(range(start, end + 1))
    result[index] = total

def main():
    threads = []
    num_threads = 10
    result = [0] * num_threads
    total_numbers = 1000000
    chunk_size = total_numbers // num_threads
    start_time = time()

    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_threads - 1 else total_numbers
        thread = threading.Thread(target=calculate_sum, args=(start, end, result, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print(f"Total Sum: {total_sum}")
    print(f"Time taken: {time() - start_time}")

if __name__ == "__main__":
    main()
