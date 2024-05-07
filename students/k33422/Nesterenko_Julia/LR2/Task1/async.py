import asyncio
from time import time


result = 0

async def calculate_sum(args):
    global result
    i_from, i_to = args
    s = sum(range(i_from, i_to))
    result += s


async def main(n):
    step = 10**6 // n
    chunks = [(i, i + step) for i in range(1, 10**6, step)]
    if chunks[-1][1] != 10**6:
        chunks[-1] = (chunks[-1][0], 10**6)

    async with asyncio.TaskGroup() as tg:
        for chunk in chunks:
            tg.create_task(calculate_sum(chunk))


def check_n_splits(n):
    start = time()
    global result
    result = 0
    asyncio.run(main(n))
    print("Splits:", n)
    print("Result:", result)    
    print("Execution time:", time() - start)
    print()


if __name__ == "__main__":
    for n in range(2, 11):
        check_n_splits(n)