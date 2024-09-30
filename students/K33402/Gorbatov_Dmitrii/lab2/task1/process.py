import multiprocessing
import time

def calculate_sum(start, finish, result_list, index):
    total = 0
    for i in range(start, finish + 1):
        total += i
    result_list[index] = total  # Сохраняем результат в общий список

def multiprocessing_count():
    processes = []
    chunks = 5
    total = 1000000
    chunk_size = total // chunks

    # Используем Manager для создания списка, который может быть разделен между процессами
    with multiprocessing.Manager() as manager:
        results = manager.list([0] * chunks)

        start_time = time.time()
        for i in range(chunks):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size
            process = multiprocessing.Process(target=calculate_sum, args=(start, end, results, i))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()

        final_result = sum(results)
        print(f"Result: {final_result}")
        print(f"Multiprocessing time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    multiprocessing_count()
