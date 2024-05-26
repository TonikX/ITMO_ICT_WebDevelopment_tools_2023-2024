from datetime import datetime
import time

start_time = datetime.now()

def calculate_sum(start: int, end: int) -> int:
    total = 0
    for i in range(start, end):
        total += i*i

    time.sleep(1)
    return total

data = [
    (0, 10000000),
    (10000000, 20000000),
    (20000000, 30000000),
    (30000000, 40000000),
    (40000000, 50000000),
    (50000000, 60000000)
]

results = []
for start, end in data:
    results.append(calculate_sum(start, end))

print(f'Time taken: {datetime.now() - start_time}')
print(results)