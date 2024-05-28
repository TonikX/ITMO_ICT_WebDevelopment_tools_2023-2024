from multiprocessing import Pool


def calculate_sum(args):
    start, end = args
    total = 0
    for i in range(start, end):
        total += i
    return total

def distribution_pool():
    p = Pool(4)
    result = sum(p.imap(calculate_sum, [[1, 250001], [250001, 500001], [500001, 750001], [750001, 1000001]]))
    return result

if __name__ == "__main__":
    import time

    start_time = time.time()
    distribution_pool()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")