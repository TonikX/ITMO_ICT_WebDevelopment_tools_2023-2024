from parsing import URLS2, parse_and_save
from time import time
from multiprocessing import Pool

def main():
    NUMBER_OF_PROCESSES = 4
    
    with Pool(NUMBER_OF_PROCESSES) as pool:
        pool.map(parse_and_save, URLS2)

if __name__ == "__main__":
    start = time()
    main()
    end = time()
    print("Time: " + str(end - start))