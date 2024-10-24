from time import time



def calculate_sum(start: int, end: int) -> int:
    '''
    function to calculate the sum of int numbers falling between the range [a,b]

    params
    -----
    start - the start of the interval
    end - the end of the interval
    '''
    sum = 0
    for i in range(start, end + 1):
        sum += i
    return sum

start_time = time()
print(calculate_sum(1, 1000000))
print(f'time: {time() - start_time}')