from base import AbstractBaseSumCalculator
import time
import threading


class ThreadingSumCalculator(AbstractBaseSumCalculator):
    def __str__(self):
        return "ThreadingSumCalculator"
    
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
        results = []

        def worker(task):
            partial_sum = self.calculate_range_sum(task)
            results.append(partial_sum)

        threads = []

        for task in self.tasks:
            thread = threading.Thread(target=worker, args=(task,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        total_sum = sum(results)
        return total_sum


if __name__ == '__main__':
    calc = ThreadingSumCalculator(number=100, n_splits=10, time_to_sleep=0.001)
    calc.run_experiments()
