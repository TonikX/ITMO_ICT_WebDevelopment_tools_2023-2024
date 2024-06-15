import threading

from task2.abstract_worker import AbstractWorker


class ThreadingWorker(AbstractWorker):
    def run(self):
        tasks = self._aggregate_tasks_for_range(self._create_thread)

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

    def _create_thread(self, urls: list[str]) -> threading.Thread:
        return threading.Thread(target=self._sync_process_urls, args=(urls,))
