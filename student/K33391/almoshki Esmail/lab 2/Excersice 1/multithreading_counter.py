import threading
from time import time 
import numpy as np

def calculate_sum(start: int, end: int, arr:np.ndarray) -> int:
    '''
    function to calculate the sum of int numbers falling between the range [a,b]

    params
    -----
    start - the start of the interval
    end - the end of the interval
    '''
    # print(f"{start} to {end}")
    sum = 0
    for i in range(start, end + 1):
        sum += i
    arr.append(sum)
    return sum



threads = []
sums = []
start_time = time()

for i in range(0, 4):
    thread = threading.Thread(target=calculate_sum, args=(
        (250000 * i) + 1, 250000 * (i + 1), sums))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
print(f'time: {time() - start_time}')
print(sum(sums))
