from parsing import URLS2, parse_and_save
from time import time
from threading import Thread

def main():
    threads = []

    for i in range(len(URLS2)):
        thread = Thread(target=parse_and_save, args=(URLS2[i], ))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print("Time: " + str(end - start))