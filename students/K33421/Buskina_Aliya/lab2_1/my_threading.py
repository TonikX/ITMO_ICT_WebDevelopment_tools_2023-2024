import threading
import time

def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)

def main():
    result = []
    thread1 = threading.Thread(target=calculate_sum, args=(1, 500001, result))
    thread2 = threading.Thread(target=calculate_sum, args=(500001, 1000001, result))

    start_time = time.time()

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    total_sum = sum(result)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Total sum using threading:", total_sum)
    print("Execution time:", execution_time, "seconds")

if __name__ == "__main__":
    main()
