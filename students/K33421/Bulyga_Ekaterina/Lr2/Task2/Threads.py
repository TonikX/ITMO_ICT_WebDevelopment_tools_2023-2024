from parser import parse
import threading
import time


def main():
    threads = [threading.Thread(target=parse, args=(season_start, season_start + 4, year)) for season_start, year in zip(range(226, 241, 5), range(2008, 2024, 5))]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


time_start = time.time()
main()
print(time.time() - time_start)
# 199.98758697509766
