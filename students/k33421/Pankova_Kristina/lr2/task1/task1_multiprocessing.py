import multiprocessing

def calculate_sum(numbers):
    total_sum = sum(numbers)
    print(f"Total sum: {total_sum}")

def main():
    numbers = list(range(1, 1000001))
    num_processes = 4
    chunk_size = len(numbers) // num_processes
    processes = []

    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i != num_processes - 1 else len(numbers)
        process = multiprocessing.Process(target=calculate_sum, args=(numbers[start:end],))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print(f"Execution time: {time.time() - start_time} seconds")
