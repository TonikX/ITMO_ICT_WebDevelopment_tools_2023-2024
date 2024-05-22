import threading


def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)


def main():
    num_threads = 4
    chunk_size = 1000000 // num_threads
    threads = []
    result = []

    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size + 1
        thread = threading.Thread(target=calculate_sum, args=(start, end, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print("Total sum:", total_sum)


if __name__ == "__main__":
    import time

    start_time = time.time()
    main()
    print("Execution time:", time.time() - start_time)
