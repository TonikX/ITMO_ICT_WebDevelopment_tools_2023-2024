import threading
from task2.settings import URLS
from naive import parse_and_save
import time

threads = []

start_time = time.time()

for url in URLS[:31]:
    thread = threading.Thread(target=parse_and_save, args=(url,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(time.time() - start_time)
