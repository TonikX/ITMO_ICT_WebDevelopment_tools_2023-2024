import multiprocessing
import time


def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.put(total)


def main():
    result = multiprocessing.Queue()
    processes = []

    for i in range(20):
        start = i * 50000 + 1
        end = (i + 1) * 50000 + 1
        process = multiprocessing.Process(
            target=calculate_sum, args=(start, end, result)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = sum([result.get() for _ in range(result.qsize())])
    print("Total sum:", total_sum)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Multiprocessing time: {time.time() - start_time}")
