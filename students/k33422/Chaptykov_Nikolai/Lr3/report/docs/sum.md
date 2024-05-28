# База сумматора
Задача: Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных задач для ускорения выполнения.
Импортируем необходимые библиотеки:
```Python
import threading
import asyncio
import multiprocessing
from typing import Tuple, List
import numpy as np
import time
import sys
```
Реализуем базовый класс, который в дальнейшем будет использоваться реализациями сумматора на библиотеке threading, asyncio и multiprocessing:
```Python
class SumCalc:
    def __init__(self, n: int, split_num: int):
        """
        Создаем искусственные таски для дальнейших вычислений.
        В каждом кортеже итогового списка хранятся попарно все
        четные числа от 0 до n включительно, по парам значений
        в дальнейшем будут высчитыватся нечетные числа, находящиеся
        между ними: 
        [2, 4, 6],
        2 + 4 / 2 = 3,
        4 + 6 / 2 = 5,
        [2, 3, 4, 5, 6]
        """
        even_lst = [(num - 2, num) for num in range(2, n + 1, 2)]
        self.tasks = np.array_split(even_lst, split_num)
        self.sum = np.int64(n)

    def run(self):
        start = time.time()
        self._calculate()
        end = time.time()
        return f"Время выполнения {self}: {end - start} секунд, сумма: {self.sum} у.е."
```