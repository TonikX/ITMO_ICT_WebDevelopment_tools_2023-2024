from multiprocessing import Process, Queue
import time

def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.put(partial_sum)

def main():
    result = Queue()
    process1 = Process(target=calculate_sum, args=(1, 500001, result))
    process2 = Process(target=calculate_sum, args=(500001, 1000001, result))

    start_time = time.time()

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    total_sum = 0
    while not result.empty():
        total_sum += result.get()

    end_time = time.time()
    execution_time = end_time - start_time

    print("Total sum using multiprocessing:", total_sum)
    print("Execution time:", execution_time, "seconds")

if __name__ == "__main__":
    main()
