# Реализации сумматоров
Напишем реализацию сумматора на потоках:
```Python
class ThreadCalc(SumCalc):  # реализация на потоках
    def __str__(self):
        return "ThreadCalc"

    def _thread_target(self, chunk: List[Tuple[int, int]]):
        temp_sum = 0
        for tup in chunk:
            temp_sum = np.int64(
                np.add(tup[0] + (tup[0] + tup[1]) // 2, temp_sum))
        self.sum = np.add(temp_sum, self.sum)

    def _calculate(self):
        ths = []
        for chunk in self.tasks:
            th = threading.Thread(target=self._thread_target, args=(chunk,))
            ths.append(th)
            th.start()

        for th in ths:
            th.join()
        sys.stdout.write("\b" * 7)  # удаляет спиннер
```
Напишем реализацию сумматора на asyncio:
```Python
class AsyncCalc(SumCalc):  # реализация на Asyncio
    def __str__(self):
        return "AsyncCalc"

    async def _async_target(self, chunk: List[Tuple[int, int]]):
        temp_sum = 0
        for tup in chunk:
            temp_sum = np.int64(
                np.add(tup[0] + (tup[0] + tup[1]) // 2, temp_sum))
        self.sum = np.add(temp_sum, self.sum)

    async def _calculate_async(self):
        tasks = []
        for chunk in self.tasks:
            task = asyncio.create_task(self._async_target(chunk))
            tasks.append(task)
        await asyncio.gather(*tasks)

    def _calculate(self):
        asyncio.run(self._calculate_async())
        sys.stdout.write("\b" * 7)  # удаляет спиннер
```
Напишем реализацию сумматора на процессах:
```Python
class MultiCalc(SumCalc):  # реализация на процессах
    def __str__(self):
        return "PoolCalc"

    def _process(self, chunk: List[Tuple[int, int]]):
        temp_sum = 0
        for tup in chunk:
            temp_sum = np.int64(
                np.add(tup[0] + (tup[0] + tup[1]) // 2, temp_sum))
        return temp_sum

    def _calculate(self):
        pool = multiprocessing.Pool(len(self.tasks))
        results = pool.map(self._process, self.tasks)
        pool.close()
        pool.join()
        self.sum = np.int64(np.add(self.sum, np.sum(results)))
        sys.stdout.write("\b" * 7)  # удаляет спиннер
```
Напишем функцию, запускающую все виды вычислений:
```Python
def run_jobs(params: Tuple[int, int]):  # получает n и split_num
    global keep_spinning
    keep_spinning = True  # флаг состояния спиннера
    th = threading.Thread(target=spinning_cursor)
    th.start()
    print(ThreadCalc(*params).run())
    print(AsyncCalc(*params).run())
    print(MultiCalc(*params).run())
    keep_spinning = False
    th.join()
    sys.stdout.write("\b" * 7)
```