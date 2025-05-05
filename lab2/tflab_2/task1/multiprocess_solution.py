import multiprocessing
import time

def calculate_sum(start_end):
    start, end = start_end
    return sum(range(start, end))

def main():
    target = 1000000000
    num_processes = 5
    chunk_size = target // num_processes
    ranges = [(i * chunk_size + 1, (i + 1) * chunk_size + 1) for i in range(num_processes)]
    start_time = time.time()

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(calculate_sum, ranges)

    total_sum = sum(results)
    print(f"Количество процессов: {num_processes}")
    print(f"Счёт до {target}")
    print(f"Общая сумма: {total_sum}")
    print(f"Время выполнения при помощи multiprocessing: {time.time() - start_time:.2f} секунд")

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()
