from base import AbstractBaseSumCalculator
import time


class SimpleSumCalculator(AbstractBaseSumCalculator):
    def __str__(self):
        return "SimpleSumCalculator"
    
    def calculate_range_sum(self, start_end):
        start, end = start_end
        total_sum = 0
        current_number = start
        while current_number <= end:
            total_sum += current_number
            current_number += 1
            time.sleep(self.time_to_sleep)
        return total_sum
    
    def calculate_sum(self):
        results = [self.calculate_range_sum(task) for task in self.tasks]
        total_sum = sum(results)
        return total_sum


if __name__ == '__main__':
    calc = SimpleSumCalculator(number=100, n_splits=10, time_to_sleep=0.001)
    calc.run_experiments()