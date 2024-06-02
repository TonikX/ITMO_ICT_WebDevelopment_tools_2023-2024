from src.runners import SumCalculatorBase, run_with_args
from typing import Tuple
import multiprocessing


class SumCalculatorThreaded(SumCalculatorBase):
    def _task_executor(self, params: Tuple[int, int]) -> int:
        return self._sum_range(params[0], params[1])

    def calculate_sum(self, target: int, split_count: int) -> int:
        with multiprocessing.Pool(processes=split_count) as pool:
            results = pool.map(
                self._task_executor, self._split_to_ranges(1, target, split_count)
            )

        return sum(results)


if __name__ == "__main__":
    run_with_args(SumCalculatorThreaded())
