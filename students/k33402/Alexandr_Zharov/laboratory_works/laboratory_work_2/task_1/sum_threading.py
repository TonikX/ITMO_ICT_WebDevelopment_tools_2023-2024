import threading


def calculate_sum(start, end, result):
    partial_sum = sum(range(start, end))
    result.append(partial_sum)


def main():
    result = []
    threads = []
    chunk_size = 100000

    for i in range(0, 1000000, chunk_size):
        thread = threading.Thread(target=calculate_sum, args=(i + 1, i + chunk_size + 1, result))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print("Конечный результат:", total_sum)

if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print("Затраченное время:", time.time() - start_time)
