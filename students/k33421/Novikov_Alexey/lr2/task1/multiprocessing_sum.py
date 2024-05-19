import multiprocessing
import time


def calculate_partial_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))


def calculate_sum() -> None:
    start_time = time.time()

    with multiprocessing.Pool(processes=4) as pool:
        results = pool.starmap(
            calculate_partial_sum,
            [(1, 250000), (250001, 500000), (500001, 750000), (750001, 1000000)]
        )

    total_sum = sum(results)

    print(
        f"Сумма: {total_sum}\n"
        f"Время: {time.time() - start_time}"
    )


if __name__ == "__main__":
    calculate_sum()
