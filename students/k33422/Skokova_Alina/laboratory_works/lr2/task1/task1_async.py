import asyncio
import time


async def calculate_sum(beg, end):
    counter = 0
    for i in range(beg, end):
        counter += i
    return counter


async def main(num):
    beg = 1
    step = int(1000000 / num)
    calculate_tasks = []
    start = time.time()
    for i in range(num):
        end = beg + step
        beg_new = beg
        beg = end
        calculate_task = asyncio.create_task(calculate_sum(beg_new, end))
        calculate_tasks.append(calculate_task)
    answers = await asyncio.gather(*calculate_tasks)
    finish = time.time() - start
    print(f'Counter value: {sum(answers)}; time: {round(finish, 4)}; number of tasks: {num}')

if __name__ == '__main__':
    task_nums = [2, 4, 8, 10, 25]
    for task_num in task_nums:
        asyncio.run(main(task_num))