import math
from typing import Callable, Any


class AbstractWorker:
    _start: int

    _end: int

    _n_tasks: int

    def __init__(self, start: int, end: int, n_tasks: int):
        self._start = start
        self._end = end
        self._n_tasks = n_tasks

    def run(self):
        raise NotImplementedError()

    def _calc_range(self, start: int, end: int, task_i: int) -> int:
        summ = 0

        for i in range(start, end):
            summ += i

        return summ

    def _aggregate_tasks_for_range(self, create_task: Callable[[int, int, int], Any]) -> list:
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
