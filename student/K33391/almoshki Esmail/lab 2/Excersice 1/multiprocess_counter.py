import multiprocessing
from time import time


def calculate_sum(start: int, end: int, arr) -> int:
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
    arr.append(sum)
    return sum

def main():
  processes = []
  nums = multiprocessing.Manager().list()
  start_time = time()

  for i in range(0, 4):
      process = multiprocessing.Process(target=calculate_sum, args=(
          (250000 * i) + 1, 250000 * (i + 1), nums))

      processes.append(process)
      process.start()

  for process in processes:
      process.join()
  print(f'time: {time() - start_time}')
  print(sum(nums))


if __name__ == "__main__":
    main()