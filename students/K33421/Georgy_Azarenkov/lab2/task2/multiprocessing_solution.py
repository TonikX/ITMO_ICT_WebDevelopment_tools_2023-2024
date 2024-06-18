import multiprocessing
from multiprocessing import Manager

from task2.abstract_solution import AbstractSolution


class MultiprocessingSolution(AbstractSolution):
    def __init__(self, n_tasks, urls):
        super().__init__(n_tasks, urls)
        self._manager = Manager()

    def run(self):
        tasks = self._aggregate_tasks_for_range(self._create_process)

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

    def _create_process(self, urls):
        return multiprocessing.Process(target=self._sync_process_urls, args=(urls,))
