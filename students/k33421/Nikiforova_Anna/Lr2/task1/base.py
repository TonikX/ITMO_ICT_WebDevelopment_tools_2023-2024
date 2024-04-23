from abc import ABC, abstractmethod
import statistics
import time
import asyncio
from tqdm import tqdm
from typing import List, Tuple


class BaseSumCalculator(ABC):
    def __init__(self, number: int = 1_000_000, n_splits: int = 10, time_to_sleep: float = 0.001) -> None:
        self.number: int = number
        self.n_splits: int = n_splits
        self.time_to_sleep: float = time_to_sleep
        self.tasks: List[Tuple[int, int]] = self.split_task()

    def split_task(self) -> List[Tuple[int, int]]:
        """
        >>> try:
        ...     BaseSumCalculator(7, 10).split_task()
        ... except AssertionError:
        ...     print("AssertionError raised")
        AssertionError raised
        >>> BaseSumCalculator(6, 2).split_task()
        [(1, 3), (4, 6)]
        >>> BaseSumCalculator(6, 1).split_task()
        [(1, 6)]
        >>> BaseSumCalculator(10, 3).split_task()
        [(1, 3), (4, 6), (7, 10)]
        >>> BaseSumCalculator(11, 3).split_task()
        [(1, 3), (4, 6), (7, 11)]
        >>> BaseSumCalculator(100, 5).split_task()
        [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
        """
        if self.n_splits > self.number:
            raise AssertionError("Number of splits cannot exceed the number itself.")
        chunk_size: int = self.number // self.n_splits
        tasks: List[Tuple[int, int]] = []
        start: int = 1
        for _ in range(self.n_splits):
            end: int = start + chunk_size - 1 if start + chunk_size - 1 <= self.number - chunk_size else self.number
            tasks.append((start, end))
            start += chunk_size
        return tasks

    async def calculate_sum(self) -> int:
        total_sum: int = 0
        for start, end in self.tasks:
            total_sum += await self.calculate_range_sum(start, end)
        return total_sum

    def run_one_experiment(self, is_async: bool = False) -> Tuple[int, float]:
        start_time: float = time.time()
        calculated_sum: int = asyncio.run(self.calculate_sum()) if is_async else self.calculate_sum()
        end_time: float = time.time()
        execution_time: float = end_time - start_time
        return calculated_sum, execution_time

    def run_experiments(self, num_iterations: int = 20, is_async: bool = False, verbose = True) -> float:
        times: List[float] = []

        for _ in tqdm(range(num_iterations)):
            _, execution_time = self.run_one_experiment(is_async=is_async)
            times.append(execution_time)

        median_time = statistics.median(times)
        if verbose:
            print("Median time:", median_time) 
        return median_time


class AbstractBaseSumCalculator(BaseSumCalculator):
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass
    
    @abstractmethod
    async def calculate_range_sum(self, start: int, end: int) -> int:
        pass

    @abstractmethod
    def calculate_sum(self) -> int:
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
