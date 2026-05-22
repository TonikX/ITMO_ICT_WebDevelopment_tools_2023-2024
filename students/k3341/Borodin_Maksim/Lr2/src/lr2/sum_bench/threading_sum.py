import threading
import time

N = 1_000_000
WORKERS = 4


def calculate_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))


def run(workers: int = WORKERS) -> dict:
    chunk = N // workers
    parts = [0] * workers
    threads: list[threading.Thread] = []

    def worker(index: int, left: int, right: int) -> None:
        parts[index] = calculate_sum(left, right)

    started = time.perf_counter()
    for index in range(workers):
        left = index * chunk + 1
        right = N if index == workers - 1 else (index + 1) * chunk
        thread = threading.Thread(target=worker, args=(index, left, right))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    elapsed = time.perf_counter() - started

    total = sum(parts)
    return {"mode": "threading", "workers": workers, "result": total, "elapsed_sec": elapsed}


if __name__ == "__main__":
    output = run()
    print(output)
