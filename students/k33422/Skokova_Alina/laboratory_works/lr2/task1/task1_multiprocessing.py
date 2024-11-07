from multiprocessing import Process, Queue
import time


def calculate_sum(beg, end, q):
    counter = 0
    for i in range(beg, end):
        counter += i
    q.put(counter)


def main(num):
    q = Queue()
    processes = []
    beg = 1
    step = int(1000000 / num)
    for i in range(num):
        end = beg + step
        processes.append(Process(target=calculate_sum, args=(beg, end, q,)))
        beg = end
    start = time.time()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    finish = time.time() - start
    answer = 0
    while not q.empty():
        answer += q.get()
    print(f'Counter value: {answer}; time: {round(finish, 4)}; number of processes: {num}')

if __name__ == '__main__':
    process_nums = [2, 4, 8, 10, 25]
    for process_num in process_nums:
      main(process_num)