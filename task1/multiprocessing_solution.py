import multiprocessing
from multiprocessing import Manager

from task1.abstract_solution import AbstractSolution


class MultiprocessingSolution(AbstractSolution):
    def __init__(self, start, end, n_tasks):
        super().__init__(start, end, n_tasks)
        self._manager = Manager()
        self._results = self._manager.list([0] * n_tasks)

    def run(self):
        tasks = self._aggregate_tasks_for_range(self._create_process)

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

        return sum(self._results)

    def _create_process(self, start, end, task_i):
        return multiprocessing.Process(
            target=self._calc_range_and_put_in_given_results,
            args=(self._results, start, end, task_i)
        )

    @staticmethod
    def _calc_range_and_put_in_given_results(results, start, end, task_i):
        summ = 0

        for i in range(start, end):
            summ += i

        results[task_i] = summ
