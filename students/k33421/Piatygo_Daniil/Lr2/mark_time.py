import time


def mark_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Общее время выполнения: {end_time - start_time} секунд.")
        return result

    return wrapper
