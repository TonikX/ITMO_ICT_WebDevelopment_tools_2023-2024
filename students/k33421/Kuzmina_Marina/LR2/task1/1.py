import threading
import time

start_time = time.time()
def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.append(total)

if __name__ == "__main__":
    result = []
    threads = []
    num_threads = 4
    chunk_size = 1000000 // num_threads
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1
        thread = threading.Thread(target=calculate_sum, args=(start, end, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print("Total sum using threading:", total_sum)

end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения программы: {execution_time} секунд")