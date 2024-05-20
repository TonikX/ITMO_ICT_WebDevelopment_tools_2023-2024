import asyncio

from task1.abstract_solution import AbstractSolution


class AsyncSolution(AbstractSolution):
    def run(self):
        return asyncio.run(self._run())

    async def _run(self):
        tasks = self._aggregate_tasks_for_range(self._async_calc_range)
        return sum(await asyncio.gather(*tasks))

    async def _async_calc_range(self, start, end, n_tasks):
        summ = 0

        for i in range(start, end):
            summ += i

        return summ
