from multiprocessing import Process, Queue


def calculate_sum(start, end, result_queue):
    partial_sum = sum(range(start, end))
    result_queue.put(partial_sum)


def main():
    result_queue = Queue()
    processes = []
    chunk_size = 100000

    num = 1_000_000
    for i in range(0, num, chunk_size):
        process = Process(target=calculate_sum, args=(i+1, i+chunk_size+1, result_queue))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    total_sum = 0
    while not result_queue.empty():
        total_sum += result_queue.get()

    print("Result:", total_sum)

if __name__ == "__main__":
    print("MUTLIPROCESS")
    import time
    start_time = time.time()
    main()
    print("Time:", time.time() - start_time)
