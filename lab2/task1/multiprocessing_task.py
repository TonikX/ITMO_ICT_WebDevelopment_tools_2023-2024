import multiprocessing
import time

num = 5
number = 1000000

def calculate_sum(start, end, results, index):
    summ = 0
    for i in range(start, end + 1):
        summ += i
    results[index] = summ

def Sum_multiprocessing():
    processes = []
    chunk_size = number // num
    manager = multiprocessing.Manager()
    result = manager.list([0] * num)
    start_time = time.time()

    for i in range(num):
        start = i * chunk_size + 1
        end = start + chunk_size - 1
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, result, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()

    print(f"Сумма: {sum(result)}")
    print(f"Время: {end_time - start_time:.5f} секунд")

if __name__ == "__main__":
    Sum_multiprocessing()
