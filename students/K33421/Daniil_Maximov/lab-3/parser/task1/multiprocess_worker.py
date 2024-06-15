import multiprocessing
from multiprocessing import Manager, managers

from task1.abstract_worker import AbstractWorker


class MultiprocessWorker(AbstractWorker):
    _manager: Manager

    _results: list[int]

    def __init__(self, start: int, end: int, n_tasks: int):
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

    def _create_process(self, start: int, end: int, task_i: int):
        return multiprocessing.Process(
            target=self._calc_range_and_put_in_given_results,
            args=(self._results, start, end, task_i)
        )

    @staticmethod
    def _calc_range_and_put_in_given_results(results: list[int], start: int, end: int, task_i: int):
        summ = 0

        for i in range(start, end):
            summ += i

        results[task_i] = summ
