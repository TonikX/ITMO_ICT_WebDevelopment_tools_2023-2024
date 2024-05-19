import threading
import time


class SumThread(threading.Thread):
    def __init__(self, start_value: int, end_value: int) -> None:
        super().__init__()
        self.start_value = start_value
        self.end_value = end_value
        self.result = 0

    def run(self) -> None:
        self.result = sum(range(self.start_value, self.end_value + 1))


def calculate_sum() -> None:
    start_time = time.time()

    threads = [
        SumThread(1, 250000),
        SumThread(250001, 500000),
        SumThread(500001, 750000),
        SumThread(750001, 1000000),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = 0
    for thread in threads:
        total_sum += thread.result

    print(
        f"Сумма: {total_sum}\n"
        f"Время: {time.time() - start_time}"
    )


if __name__ == "__main__":
    calculate_sum()
