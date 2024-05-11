from src.runners import SumCalculatorBase, run_with_args


class SumCalculatorSimple(SumCalculatorBase):
    def calculate_sum(self, target: int, split_count: int):
        return self._sum_range(1, target)


if __name__ == "__main__":
    run_with_args(SumCalculatorSimple())
