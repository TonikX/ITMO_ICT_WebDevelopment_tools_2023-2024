import asyncio
from time import time


# функция подсчета суммы в заданном диапозоне
async def calculate_sum(start, end):
    s = sum(range(start, end + 1))
    return s


async def main():
    start_time = time()  # засекаем начальное время
    task_count = 5  # выполняться программа будет в 5 корутин
    numbers_per_task = 1_000_000 // task_count  # в каждой корутине будет считаться сумма 200_000 чисел
    tasks = list()  # создаем список корутин, где будут они храниться

    for i in range(task_count):  # проходимся циклом и запускаем корутины
        start = i * numbers_per_task + 1  # первый индекс вычисляемого интервала
        end = start + numbers_per_task - 1  # последний индекс вычисляемого интервала
        tasks.append(calculate_sum(start, end))  # добавляем к списку асинхронную функцию подсчета

    results = await asyncio.gather(*tasks)  # ожидаем выполнения всех заданий асинхронно
    total_sum = sum(results)  # считаем сумму тех 5 сумм
    end_time = time()  # засекаем конечное время

    print(f"Сумма: {total_sum}")  # выводим сумму
    print(f"Время выполнения: {end_time - start_time}")  # выводим время выполнения


if __name__ == "__main__":
    asyncio.run(main())
