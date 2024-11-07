import threading
import time

counter = 0
lock = threading.Lock()

def calculate_sum(beg, end):
    global counter
    for i in range(beg, end):
        lock.acquire()
        counter += i
        lock.release()


def main(num):
    global counter
    threads = []
    beg = 1
    step = int(1000000 / num)
    for i in range(num):
        end = beg + step
        threads.append(threading.Thread(target=calculate_sum, args=(beg, end, )))
        beg = end
    start = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    finish = time.time() - start
    print(f'Counter value: {counter}; time: {round(finish, 4)}; number of threads: {num}')
    counter = 0


if __name__ == '__main__':
    thread_nums = [2, 4, 8, 10, 25]
    for thr in thread_nums:
      main(thr)