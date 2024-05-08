import multiprocessing
import time


def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.put(partial_sum)


def main():
    result = multiprocessing.Queue()
    start_time = time.time()
    process1 = multiprocessing.Process(target=calculate_sum, args=(1, 500001, result))
    process2 = multiprocessing.Process(target=calculate_sum, args=(500001, 1000001, result))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    total_sum = 0
    while not result.empty():
        total_sum += result.get()

    end_time = time.time()
    print("Total sum using multiprocessing:", total_sum)
    print("Time taken:", end_time - start_time, "seconds")


if __name__ == "__main__":
    main()
