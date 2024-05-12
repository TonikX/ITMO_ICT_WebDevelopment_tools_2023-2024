import threading
import time

def calculate_sum(start, end):
    return sum(range(start, end + 1))


def main_threading(total_numbers=1000000, ts=4):
    threads = []
    results = [0] * ts
    part = total_numbers // ts

    def worker(part_id):
        start = part_id * part + 1
        end = (part_id + 1) * part if part_id != (ts - 1) else total_numbers
        results[part_id] = calculate_sum(start, end)

    for i in range(ts):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)
    print(f"Total sum is: {total_sum}")


if __name__ == "__main__":
    start_time = time.perf_counter()
    main_threading()
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time} секунд")