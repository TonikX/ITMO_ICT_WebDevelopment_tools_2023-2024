import random
import threading
from time import time
import pandas as pd

from parse_basic import *


def parse_chunk(chunk):
    for key, url in chunk:
        parse_and_save(key, url)


def check_n_splits(n):
    print(n, "SPLITS")
    start = time()
    keys = list(URLS.keys())
    random.shuffle(keys)
    chunks = [keys[i:i + len(URLS) // n] for i in range(0, len(URLS), len(URLS) // n)]
    chunks = [[(k, URLS[k]) for k in c] for c in chunks]
    threads = [threading.Thread(target=parse_chunk, kwargs={"chunk": chunk}) 
                                for chunk in chunks]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return n, time() - start


if __name__ == "__main__": 
    results = {}
    for n in [2, 3, 6]:
        splits, extime = check_n_splits(n)
        results[splits] = extime
    print(pd.DataFrame({"Splits": results.keys(), "Execution Time": results.values()}))
    print()

