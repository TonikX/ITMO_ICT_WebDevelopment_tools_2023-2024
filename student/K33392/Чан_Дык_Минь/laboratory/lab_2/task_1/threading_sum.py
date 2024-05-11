import threading
import time

NUM_THREADS = 10
NUMBERS = 1000000

def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)

def get_range(i, chunk_size):
    start = i * chunk_size + 1
    end = start + chunk_size
    return start, end


def main():
    chunk_size = NUMBERS // NUM_THREADS
    result = []
    threads = []

    for i in range(NUM_THREADS):
        start, end = get_range(i, chunk_size)
        thread = threading.Thread(target=calculate_sum, args=(start, end, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_sum = sum(result)
    print("Sum of the first 1000000 numbers using Threading:", final_sum)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Execution time using Threading:", time.time() - start_time)