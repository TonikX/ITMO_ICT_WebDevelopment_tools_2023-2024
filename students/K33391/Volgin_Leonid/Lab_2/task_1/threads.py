import threading
import time

lock = threading.Lock()

def calculate_sum(start, end):
    return sum(range(start, end))

def worker(start, end, result):
    answer = calculate_sum(start, end)
    lock.acquire()
    result.append(answer)
    lock.release()


print("Threading")
start_time = time.time()

tasks = 7
total = 1000000
step = total // tasks
threads = []
results = []

start = 1
end = step + total % tasks + 1

for i in range(tasks):
    thread = threading.Thread(target=worker, args=(start, end, results))
    start = end
    end = end + step
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

total_answer = sum(results)
print(f"Total: {total_answer}")

end_time = time.time()
print(f"Time: {end_time - start_time} seconds")
print("Гаусс справился бы быстрее")