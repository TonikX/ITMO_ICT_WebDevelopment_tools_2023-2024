# Calculate threading

```
[Running] python -u "c:\Users\Alice\Desktop\shara\ITMO\Web 2 sem\local\Lab2\task1\calc_threading.py"
Calculation Result: 8000002000000
Correct result (by formula): 8000002000000
Is result correct: yes
Calculation time: 229.114 ms
```


```
import threading as thr
import time
import sys

lock = thr.Lock()
result = 0
```
Эта функция рекурсивно вычисляет сумму чисел в диапазоне от start до end. Если диапазон слишком мал (100,000 или меньше), она вычисляет сумму напрямую. В противном случае она разделяет диапазон пополам, создает два дочерних потока для вычисления суммы в каждой половине, ждет их завершения, а затем суммирует результаты.
```
def calculate_sum(start: int, end: int):
    global result

    # Process simple cases
    if end < start:
        raise Exception("Incorrect input")
    elif end - start <= 100000:
        # Use lock to modify global result variable
        cur_sum = sum(range(start, end + 1))

        with lock:
            result += cur_sum

        return cur_sum

    # Split range into two halves
    half = (end + start) // 2
    threads = [
        thr.Thread(target=calculate_sum, args=(start, half)),
        thr.Thread(target=calculate_sum, args=(half + 1, end))
    ]
    # Start threads
    for thread in threads:
        thread.start()
    # Join threads, wait until they ends
    for thread in threads:
        thread.join()
```
Этот блок кода является точкой входа программы. Он:  
- Получает входное значение calc_end из аргументов командной строки, если оно предоставлено, в противном случае использует значение по умолчанию 4,000,000.  
- Вызывает функцию calculate_sum(1, calc_end) для вычисления суммы.  
- Вычисляет правильный результат с помощью формулы (calc_end * (calc_end + 1)) // 2.  
- Выводит вычисленный результат, правильный ответ и время выполнения вычислений.
```
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        calc_end = int(sys.argv[1])
    else:
        calc_end = 4_000_000

    start_time = time.time()
    calculate_sum(1, calc_end)
    end_time = time.time()

    print("Calculation Result:", result)

    formula_result = (calc_end * (calc_end + 1)) // 2
    print("Correct result (by formula):", formula_result)
    print("Is result correct:", "yes" if result == formula_result else "no")
    print(f"Calculation time: {(end_time - start_time) * 1000:.3f} ms")
```