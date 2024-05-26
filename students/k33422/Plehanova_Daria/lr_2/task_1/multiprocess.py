import multiprocessing
import time

START = 1
END = 1_000_000_00
TASKS = 10
STEP = (END - START + 1) // TASKS


def calculate_sum(start, end):
    return sum(range(start, end))


def worker(start, end, results, i):
    results[i] = calculate_sum(start, end)


def main():
    results = multiprocessing.Manager().list([0] * TASKS)

    processes = [
        multiprocessing.Process(
            target=worker,
            args=(
                START + i * STEP,
                START + (i + 1) * STEP,
                results,
                i
            )
        )
        for i in range(TASKS)
    ]

    start_time = time.perf_counter()
    for i in processes:
        i.start()
    for i in processes:
        i.join()
    result = sum(results)
    end_time = time.perf_counter()

    print(f'Finished in {end_time - start_time:.3f} seconds')
    print(f'Result: {result}')


if __name__ == '__main__':
    main()
