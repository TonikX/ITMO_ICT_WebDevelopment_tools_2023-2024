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

=== "abstract"
    ```Python title="abstract_solution.py"
    --8<-- "lab2/task1/abstract_solution.py"
    ```

=== "async"

    ```Python title="async_solution.py"
    --8<-- "lab2/task1/async_solution.py"
    ```

=== "multiprocess"

    ```Python title="multiprocess_solution.py"
    --8<-- "lab2/task1/multiprocess_solution.py"
    ```

=== "threading"

    ```Python title="threading_solution.py"
    --8<-- "lab2/task1/threading_solution.py"
    ```


=== "results"

    **Задача 1. Различия между threading, multiprocessing и async в Python.**


    | Solution            | Time (seconds)    | Result               |
    |---------------------|-------------------|----------------------|
    | AsyncSolution       | 5.758628845214844| 4999999950000000    |
    | ThreadingSolution   | 5.542584657669067| 4999999950000000    |
    | MultiprocessSolution| 2.6884446144104004 | 4999999950000000    |
