from simple_app import SimpleSumCalculator
from threading_app import ThreadingSumCalculator
from multiprocessing_app import MultiprocessingSumCalculator
from async_app import AsyncSumCalculator
import pandas as pd


if __name__ == '__main__':
    calculators = [SimpleSumCalculator, 
                   ThreadingSumCalculator,
                   MultiprocessingSumCalculator, 
                   AsyncSumCalculator]
    num_experiments = 20
    
    experiment_params = [{'number': 1_000_000, 'n_splits': 10, 'time_to_sleep': 0},
                         {'number': 100, 'n_splits': 10, 'time_to_sleep': 0.001},
                         {'number': 10, 'n_splits': 5, 'time_to_sleep': 0.001}]
    
    data = []
    for calculator in calculators:
        for params in experiment_params:
            calculator_instance = calculator(**params)
            median_time = calculator_instance.run_experiments(num_experiments, is_async=(str(calculator_instance) == 'AsyncSumCalculator'))
            
            current_data = {'calculator': calculator_instance, 'median_time': median_time, 'num_experiments': num_experiments}
            current_data.update(params)
            data.append(current_data)
            
    pd.DataFrame(data).to_csv('stats.csv')
    