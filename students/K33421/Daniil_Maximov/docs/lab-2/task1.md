# Задание 1 


???+ question "Задание"

    **Задача 1. Различия между threading, multiprocessing и async в Python.**

    **Задача:** Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных задач для ускорения выполнения.
    
    **Подробности задания:**
    1. Напишите программу на Python для каждого подхода: threading, multiprocessing и async.
    2. Каждая программа должна содержать функцию calculate_sum(), которая будет выполнять вычисления.
    3. Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова async/await и модуль asyncio.
    4. Каждая программа должна разбить задачу на несколько подзадач и выполнять их параллельно.
    5. Замерьте время выполнения каждой программы и сравните результаты.

=== "async"

    ```Python title="async_worker.py"
    --8<-- "lab-2/task1/abstract_worker.py"
    ```

=== "multiprocess"

    ```Python title="multiprocess_worker.py"
    --8<-- "lab-2/task1/multiprocess_worker.py"
    ```

=== "threading"

    ```Python title="threading_worker.py"
    --8<-- "lab-2/task1/threading_worker.py"
    ```


=== "results"

    **Задача 1. Различия между threading, multiprocessing и async в Python.**


    | Worker            | Time (seconds)    | Result               |
    |---------------------|-------------------|----------------------|
    | AsyncWorker       | 18.106175422668457| 79999999800000000    |
    | ThreadingWorker   | 18.884188413619995| 79999999800000000    |
    | MultiprocessWorker| 8.224344253540039 | 79999999800000000    |