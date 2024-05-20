import math


class AbstractSolution:
    def __init__(self, start, end, n_tasks):
        self._start = start
        self._end = end
        self._n_tasks = n_tasks

    def run(self):
        raise NotImplementedError()

    def _calc_range(self, start, end, task_i):
        summ = 0

        for i in range(start, end):
            summ += i

        return summ

    def _aggregate_tasks_for_range(self, create_task):
        chunk_size = math.ceil((self._end - self._start) / self._n_tasks)
        tasks = []

        for i in range(self._n_tasks):
            task_start = self._start + i * chunk_size
            task_end = min(self._start + (i + 1) * chunk_size, self._end)
            task = create_task(task_start, task_end, i)
            tasks.append(task)

            if task_end == self._end:
                break

        return tasks
