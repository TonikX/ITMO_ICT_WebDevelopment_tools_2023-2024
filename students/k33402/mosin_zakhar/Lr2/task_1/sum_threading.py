import threading


def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)


def main():
    result = []
    threads = []
    chunk_size = 100000

    num = 1_000_000
    for i in range(0, num, chunk_size):
        thread = threading.Thread(target=calculate_sum, args=(i + 1, i + chunk_size + 1, result))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print("Result:", total_sum)

if __name__ == "__main__":
    print("THREADING")
    import time
    start_time = time.time()
    main()
    print("Time:", time.time() - start_time)
