import asyncio
import time

# асинхронная функция, вычисляющая частичную сумму чисел от start до end
async def calculate_partial_sum(start, end):
    return sum(range(start, end + 1))

# главная асинхронная функция, распределяющая работу и собирающая результаты
async def calculate_sum():
    total_tasks = 5  # общее количество задач
    n = 1000000  # верхняя граница диапазона
    step = n // total_tasks  # шаг для разделения диапазона на части
    tasks = []

    # создаем задачи для вычисления частичных сумм
    for i in range(total_tasks):
        start = i * step + 1  # начало диапазона для текущей задачи
        end = (i + 1) * step if i != total_tasks - 1 else n  # конец диапазона для текущей задачи
        tasks.append(asyncio.create_task(calculate_partial_sum(start, end)))

    # ожидаем завершения всех задач и собираем результаты
    results = await asyncio.gather(*tasks)
    total_sum = sum(results)  # суммируем результаты всех задач
    return total_sum

start_time = time.time()
sum_result = asyncio.run(calculate_sum())  # запускаем асинхронную функцию
end_time = time.time()
print(f"sum: {sum_result}, time: {end_time - start_time} seconds")  # выводим результат и время выполнения
