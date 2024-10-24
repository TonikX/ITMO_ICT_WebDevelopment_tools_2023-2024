import multiprocessing

def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.put(total)

def main():
    result = multiprocessing.Queue()
    processes = []
    chunk_size = 100000

    for i in range(0, 1000000, chunk_size):
        process = multiprocessing.Process(target=calculate_sum, args=(i+1, i+chunk_size+1, result))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_sum = 0
    while not result.empty():
        final_sum += result.get()

    print("Sum:", final_sum)

if __name__ == "__main__":
    main()

