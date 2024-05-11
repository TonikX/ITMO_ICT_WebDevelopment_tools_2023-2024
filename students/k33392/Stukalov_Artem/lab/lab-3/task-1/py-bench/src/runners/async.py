from src.runners import SumCalculatorBaseAsync, run_with_args_async
from typing import Tuple
import asyncio


class SumCalculatorThreaded(SumCalculatorBaseAsync):
    async def _sum_range_with_sleep(self, params: Tuple[int, int]) -> int:
        res = 0
        for x in range(params[0], params[1] + 1):
            res += x
        return res

    async def _task_executor(self, params: Tuple[int, int]) -> int:
        return await self._sum_range_with_sleep(params)

    async def calculate_sum(self, target: int, split_count: int) -> int:
        tasks = [
            asyncio.create_task(self._task_executor(params))
            for params in self._split_to_ranges(1, target, split_count)
        ]
        results = await asyncio.gather(*tasks)
        return sum(results)


if __name__ == "__main__":
    asyncio.run(run_with_args_async(SumCalculatorThreaded()))
