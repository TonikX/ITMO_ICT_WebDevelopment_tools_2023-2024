import asyncio
import time

from plt_builder import paint

x = []
y = []
async def calculate_sum_of_range(start, end):
    partial_sum = sum(range(start, end))
    return partial_sum


async def calculate_sum(border, task_cnt):
    start_time = time.time()

    cnt = border // task_cnt

    tasks = []
    for i in range(task_cnt):
        start = i * cnt + 1
        end = (i + 1) * cnt + 1 if i < task_cnt - 1 else border + 1
        task = asyncio.create_task(calculate_sum_of_range(start, end))
        tasks.append(task)

    sums = await asyncio.gather(*tasks)
    result = sum(sums)

    end_time = time.time()

    x.append(task_cnt)
    y.append(end_time - start_time)

    print("Выполнено с использованием asyncio")

    print("Сумма: ", result)
    print("Время:", end_time - start_time, "с")


if __name__ == "__main__":
    border = 1000000
    for i in range(1000, 1001):
        asyncio.run(calculate_sum(border, i))
    print(x, y)
    paint(x, y, "Сумма " + str(border) + " asyncio")

