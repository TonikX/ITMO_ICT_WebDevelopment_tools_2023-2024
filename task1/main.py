import time

from task1.async_solution import AsyncSolution
from task1.multiprocessing_solution import MultiprocessingSolution
from task1.threading_solution import ThreadingSolution


def main():
    start = 0
    end = 100_000_000
    n_tasks = 8

    solutions = [
        AsyncSolution(start, end, n_tasks),
        ThreadingSolution(start, end, n_tasks),
        MultiprocessingSolution(start, end, n_tasks)
    ]

    for solution in solutions:
        print(f"Running {solution.__class__.__name__}")
        start_time = time.time()
        result = solution.run()
        end_time = time.time()
        print(solution.__class__.__name__, end_time - start_time, result)


if __name__ == '__main__':
    main()
