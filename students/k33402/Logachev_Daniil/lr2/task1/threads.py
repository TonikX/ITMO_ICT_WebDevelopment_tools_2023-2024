import threading
import time

def calculate_partial_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

def calculate_sum():
    total_threads = 4
    n = 1000000
    thread_list = []
    result = [0] * total_threads
    step = n // total_threads

    for i in range(total_threads):
        start = i * step + 1
        end = (i + 1) * step if i != total_threads - 1 else n
        thread = threading.Thread(target=calculate_partial_sum, args=(start, end, result, i))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    total_sum = sum(result)
    return total_sum

start_time = time.time()
sum_result = calculate_sum()
end_time = time.time()
print(f"Threading sum: {sum_result}, Time taken: {end_time - start_time} seconds")