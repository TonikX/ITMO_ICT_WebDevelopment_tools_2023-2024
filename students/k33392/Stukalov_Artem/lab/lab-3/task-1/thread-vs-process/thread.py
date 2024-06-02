import concurrent.futures
import time

THREADS_COUNT = 5
COUNT = 10_000_000


def cpu_bound_time(_):
    time.sleep(0.3)
    res = sum((x for x in range(COUNT)))
    return res


def cpu_bound(_):
    return sum((x for x in range(COUNT)))


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS_COUNT) as executor:
        results = executor.map(cpu_bound_time, range(THREADS_COUNT))
        return sum(results)


if __name__ == "__main__":
    main()
