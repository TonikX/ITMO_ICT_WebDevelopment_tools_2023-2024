from multiprocessing import Process, Queue
import time

start_time = time.time()
def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.put(total)

if __name__ == "__main__":
    result = Queue()
    processes = []
    num_processes = 4
    chunk_size = 1000000 // num_processes
    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1
        process = Process(target=calculate_sum, args=(start, end, result))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = 0
    while not result.empty():
        total_sum += result.get()

    print("Total sum using multiprocessing:", total_sum)

end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения программы: {execution_time} секунд")