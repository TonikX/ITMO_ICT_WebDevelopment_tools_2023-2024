import threading
import time

RESULTS = []

def calculate_sum(part_id, part, ts, total_numbers):
        start = part_id * part + 1
        end = (part_id + 1) * part if part_id != (ts - 1) else total_numbers
        global RESULTS
        RESULTS[part_id] = sum(range(start, end + 1))

def main_threading(total_numbers=1000000, ts=4):
    threads = []
    global RESULTS
    RESULTS = [0] * ts
    part = total_numbers // ts

    for i in range(ts):
        thread = threading.Thread(target=calculate_sum, args=(i, part, ts, total_numbers))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(RESULTS)
    print(f"Total sum is: {total_sum}")


if __name__ == "__main__":
    start_time = time.perf_counter()
    main_threading()
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time} секунд")