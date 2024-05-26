import random
import pandas as pd
from multiprocessing import Pool
from time import time

from parse_basic import *


def parse_chunk(chunk):
    for key, url in chunk:
        parse_and_save(key, url)


def check_n_splits(n):
    print(n, "SPLITS")
    start = time()
    keys = list(URLS.keys())
    
    with Pool(n) as p:
        random.shuffle(keys)
        chunks = [keys[i:i + len(URLS) // n] for i in range(0, len(URLS), len(URLS) // n)]
        chunks = [[(k, URLS[k]) for k in c] for c in chunks]
        p.map(parse_chunk, chunks)
    return n, time() - start


if __name__ == "__main__": 
    results = {}
    for n in [2, 3, 6]:
        splits, extime = check_n_splits(n)
        results[splits] = extime
    print(pd.DataFrame({"Splits": results.keys(), "Execution Time": results.values()}))
    print()