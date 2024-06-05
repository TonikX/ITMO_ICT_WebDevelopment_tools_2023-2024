# Calculate async

```
[Running] python -u "c:\Users\Alice\Desktop\shara\ITMO\Web 2 sem\local\Lab2\task1\calc_async.py"
Calculation Result: 8000002000000
Correct result (by formula): 8000002000000
Is result correct: yes
Calculation time: 236.038 ms
```
  
  

```
import time
import asyncio
```
Эта асинхронная функция вычисляет сумму чисел от start до end включительно.
```
async def calculate_sum(start, end):
    total = 0
    for i in range(start, end+1):
        total += i
    return total
```
Эта асинхронная функция является точкой входа программы. Она выполняет следующие действия:  
- Устанавливает общее количество чисел, которые нужно вычислить (calc_end = 4_000_000).  
- Определяет размер "блока" (chunk_size = 250,000), который будет обрабатываться отдельной асинхронной задачей  
- Вычисляет количество задач, необходимых для обработки всех чисел (num_tasks).  
- Создает список асинхронных задач (tasks), каждая из которых вычисляет сумму чисел в своем "блоке".  
- Ожидает выполнения всех задач и суммирует их результаты.  
- Вычисляет правильный результат с помощью формулы (calc_end * (calc_end + 1)) // 2.  
- Выводит вычисленный результат, правильный ответ и время выполнения вычислений.
```
async def main():
    calc_end = 4_000_000
    chunk_size = 250000

    num_tasks = calc_end // chunk_size
    
    start_time = time.time()
    
    tasks = []
    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)
    
    total = 0
    for task in tasks:
        total += await task
    
    end_time = time.time()
    
    formula_result = (calc_end * (calc_end + 1)) // 2
    print(f"Calculation Result: {total}")
    print("Correct result (by formula):", formula_result)
    print("Is result correct:", "yes" if total == formula_result else "no")
    print(f"Calculation time: {(end_time - start_time) * 1000:.3f} ms")
```
Этот блок код запускает функцию main() в асинхронном режиме с помощью asyncio.run(main()).
```
if __name__ == "__main__":
    asyncio.run(main())
```