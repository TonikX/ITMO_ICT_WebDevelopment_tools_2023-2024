from src.runners import SumCalculatorBase, run_with_args
import threading
from typing import List


class SumCalculatorThreaded(SumCalculatorBase):
    def calculate_sum(self, target: int, split_count: int) -> int:
        threads: List[threading.Thread] = []
        results = [0] * split_count

        def task_executor(start: int, end: int, index: int):
            results[index] = self._sum_range(start, end)

        for index, sum_range in enumerate(
            self._split_to_ranges(1, target, split_count)
        ):
            thread = threading.Thread(
                target=task_executor,
                args=(sum_range[0], sum_range[1], index),
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return sum(results)


if __name__ == "__main__":
    run_with_args(SumCalculatorThreaded())
