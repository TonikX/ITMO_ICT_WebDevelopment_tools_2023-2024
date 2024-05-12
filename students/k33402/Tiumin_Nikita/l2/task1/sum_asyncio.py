import asyncio
from time import time

RUNS_NUMBER = 3
CHUNKS_NUMBER = 4
NUMBER = 1000000000


async def calc(l, r):
    return sum(range(l, r))


async def main():
    tasks = []

    for i in range(CHUNKS_NUMBER):
        l = int(i * NUMBER / CHUNKS_NUMBER + 1)
        r = int(l + NUMBER / CHUNKS_NUMBER)

        task = asyncio.create_task(calc(l, r))
        tasks.append(task)

    start = time()
    res = await asyncio.gather(*tasks)
    exec_time = time() - start

    return exec_time, res


if __name__ == "__main__":
    times = []
    for i in range(RUNS_NUMBER):
        next_time, res = asyncio.run(main())
        times.append(next_time)
        print(i + 1, ' run: ', next_time, 's. RESULT: ', sum(res))
    print('Average time: ', sum(times) / len(times), 's')


