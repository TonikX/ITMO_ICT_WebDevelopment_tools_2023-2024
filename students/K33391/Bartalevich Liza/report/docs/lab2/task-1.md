# Threads vs Porcess vs Async

Сравнение перфоманса cpu-bound задач при использовании 3 подходов в python:

- multithreading
- multiprocessing
- async

Ниже приведен листинг кода, который использовался для тестирования определенного подхода. Замеры проводились при помощи утилиты `time`, замерялись `real` и `user` время. Для замеров также использовался автоматичесикй раннер тестов, который запускал каждый тест по 10 раз и выдавал медианное время.

=== "default"

    ```Python title="simple.py"
    --8<-- "lab_2/task_1/main.py"
    ```

## Результаты замеров

```
simple.py loops = 10 target_sum = 100000000 split_count = 1
real: 2.995
user: 2.98
------------------------------

threaded.py loops = 10 target_sum = 100000000 split_count = 20
real: 4.005
user: 3.975
------------------------------

multiprocess.py loops = 10 target_sum = 100000000 split_count = 20
real: 0.42
user: 6.075
------------------------------

async.py loops = 10 target_sum = 100000000 split_count = 20
real: 3.3
user: 3.29

```

## Выводы

Как можем видеть, наилучших результатов в python удалось добиться при использовании multiprocess, так как по сути это единственная честная параллелность, которой можно добиться в python из-за GIL.
