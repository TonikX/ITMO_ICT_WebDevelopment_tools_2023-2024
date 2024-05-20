import threading

from task2.abstract_solution import AbstractSolution


class ThreadingSolution(AbstractSolution):
    def run(self):
        tasks = self._aggregate_tasks_for_range(self._create_thread)

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

    def _create_thread(self, urls):
        return threading.Thread(target=self._sync_process_urls, args=(urls,))
