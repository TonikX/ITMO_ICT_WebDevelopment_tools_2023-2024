import threading
import time

def calculate_sum(start, finish, result_list, index):
    total = 0
    for i in range(start, finish + 1):
        total += i
    result_list[index] = total

def threading_count():
    threads = []
    chunks = 5
    total = 1000000
    chunk_size = total // chunks
    results = [0] * chunks

    start_time = time.time()
    for i in range(chunks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    final_result = sum(results)

    print(f"Result: {final_result}")
    print(f"Threading time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    threading_count()