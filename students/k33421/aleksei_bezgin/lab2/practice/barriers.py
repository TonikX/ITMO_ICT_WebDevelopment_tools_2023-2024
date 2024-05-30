import threading

# Создание барьера для 3 потоков
barrier = threading.Barrier(3)

def worker():
    print("Thread", threading.current_thread().name, "is waiting at the barrier")
    # Блокировка на барьере
    barrier.wait()
    print("Thread", threading.current_thread().name, "has passed the barrier")

# Создание нескольких потоков
threads = []
for i in range(3):
    thread = threading.Thread(target=worker)
    threads.append(thread)
    thread.start()

# Ожидание завершения всех потоков
for thread in threads:
    thread.join()

print("All threads have finished.")