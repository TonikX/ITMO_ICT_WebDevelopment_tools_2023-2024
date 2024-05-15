import asyncio

from task1.abstract_worker import AbstractWorker


class AsyncWorker(AbstractWorker):
    def run(self) -> int:
        return asyncio.run(self._run())

    async def _run(self) -> int:
        tasks = self._aggregate_tasks_for_range(self._async_calc_range)
        return sum(await asyncio.gather(*tasks))

    async def _async_calc_range(self, start: int, end: int, n_tasks: int) -> int:
        summ = 0

        for i in range(start, end):
            summ += i

        return summ
