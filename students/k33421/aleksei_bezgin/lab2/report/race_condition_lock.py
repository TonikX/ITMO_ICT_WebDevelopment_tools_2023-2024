import threading

counter = 0
lock = threading.Lock()

def inctement():
    global counter
    for _ in range(1000000):
        with lock:
            counter += 1


thread1 = threading.Thread(target=inctement)
thread2 = threading.Thread(target=inctement)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(f'Result: {counter}')
