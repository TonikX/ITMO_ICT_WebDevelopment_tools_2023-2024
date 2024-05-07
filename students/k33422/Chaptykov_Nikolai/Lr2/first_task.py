import threading
import asyncio
import multiprocessing
from typing import Tuple, List
import numpy as np
import time
import sys


class SumCalc:
    def __init__(self, n: int, split_num: int):
        """
        Создаем искусственные таски для дальнейших вычислений.
        В каждом кортеже итогового списка хранятся попарно все
        четные числа от 0 до n включительно, по парам значений
        в дальнейшем будут высчитыватся нечетные числа, находящиеся
        между ними
        """
        even_lst = [(num - 2, num) for num in range(2, n + 1, 2)]
        self.tasks = np.array_split(even_lst, split_num)
        self.sum = np.int64(n)

    def run(self):
        start = time.time()
        self._calculate()
        end = time.time()
        return f"Время выполнения {self}: {end - start} секунд, сумма: {self.sum} у.е."


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


def spinning_cursor():  # немного красоты
    def cursor():
        while True:
            for cursor in "|/-\\":
                yield cursor

    spinner = cursor()
    while keep_spinning:  # крутить пока флаг равен True
        sys.stdout.write("Думаю " + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b" * 7)


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


def validate_input(cmd: str, n: str, split_num: str):
    if n.isdigit() and split_num.isdigit():
        n = int(n)
        split_num = int(split_num)
    else:
        raise TypeError("Can not convert str to int")
    if split_num > n:
        raise ValueError("Split is bigger than input")
    if split_num <= 0:
        raise ValueError("Split can not be negative or zero")
    return True


if __name__ == "__main__":  # позволяет избежать множественный запуск скрипта
    if len(sys.argv) == 3 and validate_input(*sys.argv):
        print("За работу")
        params = tuple(
            map(int, sys.argv[1:])
        )  # выделение вводных параметров n, split_num
        run_jobs(params)
        print(f"Реальная сумма: {sum([i for i in range(params[0] + 1)])}")
    else:
        print("Not enough parameters")
