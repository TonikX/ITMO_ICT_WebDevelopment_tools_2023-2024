from parser import parse
import multiprocessing
import time


def main():
    pool = multiprocessing.Pool()

    results = pool.map(parse, [(season_start, season_start + 4, year) for season_start, year in zip(range(226, 241, 5), range(2008, 2024, 5))])

    pool.close()
    pool.join()


if __name__ == '__main__':
    time_start = time.time()
    main()
    print(time.time() - time_start)

# 207.05740213394165
