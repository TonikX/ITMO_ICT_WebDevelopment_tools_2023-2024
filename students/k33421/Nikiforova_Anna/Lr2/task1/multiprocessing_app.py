from base import AbstractBaseSumCalculator 
import time
import multiprocessing


class MultiprocessingSumCalculator(AbstractBaseSumCalculator):
    def __str__(self):
        return "MultiprocessingSumCalculator"
    
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
        pool = multiprocessing.Pool(processes=self.n_splits)
        results = pool.map(self.calculate_range_sum, self.tasks)
        pool.close()
        pool.join()
        total_sum = sum(results)
        return total_sum
    
    
if __name__ == '__main__':
    calc = MultiprocessingSumCalculator(number=100, n_splits=10, time_to_sleep=0.001)
    calc.run_experiments()
