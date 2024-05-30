import threading
import time

def calculate_sum(start, end):
    result = sum(range(start, end))
    print(f"sum from {start} to {end}: {result}")

def main(num_of_tasks=5, step=1000000):
    start_time = time.time()
    threads = []
    for i in range(num_of_tasks):
        t = threading.Thread(target=calculate_sum, args=(i*step+1, (i+1)*step))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"execution time: {round(time.time() - start_time, 5)} seconds")

if __name__ == "__main__":
    num_of_tasks = 10
    step = 10000000
    main(num_of_tasks, step)