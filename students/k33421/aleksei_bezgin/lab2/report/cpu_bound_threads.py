from datetime import datetime
import threading
import time

start_time = datetime.now()

def calculate_sum(start: int, end: int, results) -> None:
    total = 0
    for i in range(start, end):
        total += i*i

    time.sleep(1)
    results.append(total)

data = [
    (0, 10000000),
    (10000000, 20000000),
    (20000000, 30000000),
    (30000000, 40000000),
    (40000000, 50000000),
    (50000000, 60000000)
]

results = []

threads = []
for start, end in data:
    thread = threading.Thread(target=calculate_sum, args=(start, end, results))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(f'Time taken: {datetime.now() - start_time}')
print(results)