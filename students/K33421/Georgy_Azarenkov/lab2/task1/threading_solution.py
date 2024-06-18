import threading

from task1.abstract_solution import AbstractSolution


class ThreadingSolution(AbstractSolution):
    def __init__(self, start, end, n_tasks):
        super().__init__(start, end, n_tasks)
        self._results = [0] * n_tasks

    def run(self):
        tasks = self._aggregate_tasks_for_range(self._create_thread)

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

        return sum(self._results)

    def _create_thread(self, start, end, index):
        return threading.Thread(target=self._calc_range_and_put_in_results, args=(start, end, index))

    def _calc_range_and_put_in_results(self, start, end, task_i):
        summ = 0

        for i in range(start, end):
            summ += i

        self._results[task_i] = summ
