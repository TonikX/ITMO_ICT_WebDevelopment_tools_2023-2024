import threading
import time


def calculate_sum(start, end):
    return sum(range(start, end))


def worker(start, end, results, i):
    results[i] = calculate_sum(start, end)


def main(tasks_count, start, end):
    results = [0] * tasks_count

    tasks = []

    for i in range(tasks_count):
        tasks.append(
            threading.Thread(
                target=calculate_sum,
                args=(
                    start + i * (end - start + 1) // tasks_count,
                    start + (i + 1) * (end - start + 1) // tasks_count
                )
            )
        )

    start_time = time.perf_counter()
    for i in tasks:
        i.start()
    for i in tasks:
        i.join()
    result = sum(results)
    end_time = time.perf_counter()

    print(f'Время выполнения: {end_time - start_time:.3f} секунд')

    return result


if __name__ == '__main__':
    main(
        tasks_count=10,
        start=1,
        end=1_000_000
    )