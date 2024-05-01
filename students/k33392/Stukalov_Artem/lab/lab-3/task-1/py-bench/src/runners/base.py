from typing import Tuple, Generator, TypedDict
from abc import ABC, abstractmethod
import argparse


class RunArgs(TypedDict):
    target_sum: int
    split_count: int


class SumCalculatorBase(ABC):
    def _sum_range(self, start: int, end: int) -> int:
        return sum((i for i in range(start, end + 1)))

    def _split_to_ranges(
        self, start: int, end: int, count: int
    ) -> Generator[Tuple[int, int], None, None]:
        step = (end - start + 1) // count
        return (
            (
                start + step * (i - 1) + (1 if i != 1 else 0),
                start + step * i if i != count else end,
            )
            for i in range(1, count + 1)
        )

    @abstractmethod
    def calculate_sum(self, target: int, split_count: int) -> int: ...


class SumCalculatorBaseAsync(SumCalculatorBase):
    @abstractmethod
    async def calculate_sum(self, target: int, split_count: int) -> int: ...


def parse_args() -> RunArgs:
    parser = argparse.ArgumentParser(
        prog="Test prog",
    )
    parser.add_argument("--target_sum", required=True)
    parser.add_argument("--split_count", required=True)
    args = parser.parse_args()
    target_sum = int(args.target_sum)  # type: ignore
    split_count = int(args.split_count)  # type: ignore

    return {
        "target_sum": target_sum,
        "split_count": split_count,
    }


def run_with_args(runner: SumCalculatorBase):
    args = parse_args()
    runner.calculate_sum(target=args["target_sum"], split_count=args["split_count"])


async def run_with_args_async(runner: SumCalculatorBaseAsync):
    args = parse_args()
    await runner.calculate_sum(
        target=args["target_sum"], split_count=args["split_count"]
    )
