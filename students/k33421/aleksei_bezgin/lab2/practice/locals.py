import threading
import time

# Создаем объект локальных данных для каждого потока
local_data = threading.local()

def set_data(data):
    """
    Установка данных в объект локальных данных
    """
    local_data.value = data

def print_data():
    """
    Печать данных из объекта локальных данных
    """
    print("Data in thread {}: {}".format(threading.current_thread().name, getattr(local_data, 'value', None)))

def worker(data):
    """
    Рабочая функция для установки и печати данных
    """
    set_data(data)
    print_data()
    time.sleep(1)  # Имитация работы

def main():
    """
    Главная функция, запускающая несколько потоков
    """
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()