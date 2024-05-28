# Финальные штрихи
Наведем красоту в консоли, добавив спиннер:
```Python
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
```
Реализуем валидатор консольного ввода:
```Python
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
```
Запустим скрипт с передачей параметров. В параметрах указывается до какого числа необходимо считать сумму и количество потоков/процессов на которые надо дробить вычисления:
```Python
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

```
Стоит также упомянуть, что запуск кода через четко указанную точку входа "&#95;&#95;main__" позволяет избежать рекурсивный запуск кода из созданных процессов
