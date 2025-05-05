import threading
import time


def calculate_sum(start, end, result, index):
    result[index] = sum(range(start, end))

target = 1000000000
num_threads = 5
chunk_size = target // num_threads
threads = []
results = [0] * num_threads
start_time = time.time()

for i in range(num_threads):
    start = i * chunk_size + 1
    end = (i + 1) * chunk_size + 1
    thread = threading.Thread(target=calculate_sum, args=(start, end, results, i))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

total_sum = sum(results)

print(f"Количество потоков: {num_threads}")
print(f"Счёт до {target}")
print(f"Общая сумма: {total_sum}")
print(f"Время выполнения при помощи threading: {time.time() - start_time:.2f} секунд")
