import asyncio
from time import time


async def calculate_sum(args):
    global RESULT
    i_from, i_to = args
    s = sum(range(i_from, i_to))
    RESULT += s


async def main(n):
    step = 10**6 // n
    chunks = [(i, i + step) for i in range(1, 10**6, step)]
    if chunks[-1][1] != 10**6:
        chunks[-1] = (chunks[-1][0], 10**6)

    async with asyncio.TaskGroup() as tg:
        for chunk in chunks:
            tg.create_task(calculate_sum(chunk))


if __name__ == "__main__":
    start = time()
    RESULT = 0
    asyncio.run(main(4))
    print("Result:", RESULT, "Execution time:", time() - start)
