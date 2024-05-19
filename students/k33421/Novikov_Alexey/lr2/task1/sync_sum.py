import time


def calculate_sum() -> None:
    start_time = time.time()

    total_sum = sum(range(1, 1000000 + 1))

    print(
        f"Сумма: {total_sum}\n"
        f"Время: {time.time() - start_time}"
    )


if __name__ == "__main__":
    calculate_sum()
