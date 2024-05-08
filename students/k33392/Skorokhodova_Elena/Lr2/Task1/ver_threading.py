import threading
import time


def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)


def main():
    result = []
    start_time = time.time()
    thread1 = threading.Thread(target=calculate_sum, args=(1, 500001, result))
    thread2 = threading.Thread(target=calculate_sum, args=(500001, 1000001, result))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    total_sum = sum(result)
    end_time = time.time()
    print("Total sum using threading:", total_sum)
    print("Time taken:", end_time - start_time, "seconds")


if __name__ == "__main__":
    main()
