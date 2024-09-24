import asyncio

# Асинхронная функция, которая будет выполняться для вычисления суммы
async def calculate_sum(start, end):
    return sum(range(start, end))

async def main():
    num_tasks = 4  # Количество задач
    chunk_size = 1000000 // num_tasks  # Размер порции данных для каждой задачи
    tasks = []  # Список для хранения задач

    # Создание и запуск задач
    for i in range(num_tasks):
        start = i * chunk_size + 1  # Начальное значение для порции данных
        end = (i + 1) * chunk_size + 1  # Конечное значение для порции данных
        task = asyncio.create_task(calculate_sum(start, end))  # Создание задачи
        tasks.append(task)  # Добавление задачи в список

    partial_sums = await asyncio.gather(*tasks)  # Ожидание завершения всех задач и получение результатов
    total_sum = sum(partial_sums)  # Вычисление общей суммы
    print("Total sum:", total_sum)

if __name__ == "__main__":
    import time

    start_time = time.time()
    asyncio.run(main())
    print("Execution time:", time.time() - start_time)