from base import AbstractBaseSumCalculator
import time
import asyncio


class AsyncSumCalculator(AbstractBaseSumCalculator):
    def __str__(self):
        return "AsyncSumCalculator"
    
    async def calculate_range_sum(self, start_end):
        start, end = start_end
        total_sum = 0
        current_number = start
        while current_number < end + 1:
            total_sum += current_number
            current_number += 1
            await asyncio.sleep(self.time_to_sleep)  # Allow other tasks to run
        return total_sum

    async def calculate_sum(self):
        tasks = [asyncio.create_task(self.calculate_range_sum(task)) for task in self.tasks]
        results = await asyncio.gather(*tasks)
        total_sum = sum(results)
        return total_sum


if __name__ == '__main__':
    calc = AsyncSumCalculator(number=100, n_splits=10, time_to_sleep=0.001)
    calc.run_experiments(is_async=True)