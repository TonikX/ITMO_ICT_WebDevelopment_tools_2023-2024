import threading

# максимум 3 потока могут захватывать семафор
semaphore = threading.Semaphore(3)

def worker():
    # Захват семафора
    semaphore.acquire()
    print("Semaphore acquired by", threading.current_thread().name)
    # Имитация работы
    print("Worker is working...")
    # Освобождение семафора
    semaphore.release()
    print("Semaphore released by", threading.current_thread().name)

# Создание нескольких потоков
threads = []
for i in range(5):
    thread = threading.Thread(target=worker)
    threads.append(thread)
    thread.start()

# Ожидание завершения всех потоков
for thread in threads:
    thread.join()

print("All threads have finished.")