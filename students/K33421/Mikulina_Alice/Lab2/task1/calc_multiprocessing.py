from multiprocessing import Process, Queue
import time
import sys


def calculate_sum(start: int, end: int, queue: Queue = None):
    # Process simple cases
    if end < start:
        raise Exception("Incorrect input")
    elif end - start <= 100000:
        # Use lock to modify global result variable
        cur_sum = sum(range(start, end + 1))
        if queue:
            queue.put(cur_sum)
        return cur_sum

    if queue is None:
        queue = Queue()

    # Split range into two halves
    half = (end + start) // 2
    processes = [
        Process(target=calculate_sum, args=(start, half, queue)),
        Process(target=calculate_sum, args=(half + 1, end, queue))
    ]
    # Start threads
    for process in processes:
        process.start()
    # Join threads, wait until they ends
    for process in processes:
        process.join()

    new_value = int(queue.get()) + int(queue.get())
    queue.put(new_value)

    return new_value


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        calc_end = int(sys.argv[1])
    else:
        calc_end = 4_000_000

    start_time = time.time()
    result = calculate_sum(1, calc_end)
    end_time = time.time()

    print("Calculation Result:", result)

    formula_result = (calc_end * (calc_end + 1)) // 2
    print("Correct result (by formula):", formula_result)
    print("Is result correct:", "yes" if result == formula_result else "no")
    print(f"Calculation time: {(end_time - start_time) * 1000:.3f} ms")
