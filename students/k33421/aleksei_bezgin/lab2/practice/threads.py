import threading

counter = 0

# blocking object to avoid race condition
lock = threading.Lock()

def increment():
    global counter
    for _ in range(1000000):
        lock.acquire()
        counter += 1
        lock.release()

def decrement():
    global counter
    for _ in range(1000000):
        lock.acquire()
        counter -= 1
        lock.release()

def main():
    global counter
    thread1 = threading.Thread(target=increment)
    thread2 = threading.Thread(target=decrement)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Counter value:", counter)

if __name__ == "__main__":
    main()