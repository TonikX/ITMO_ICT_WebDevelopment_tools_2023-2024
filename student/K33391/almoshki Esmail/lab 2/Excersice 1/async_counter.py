import asyncio
from time import time

async def calculate_sum(start: int, end:int) -> int:
    '''
    function to calculate the sum of int numbers falling between the range [a,b]

    params
    -----
    start - the start of the interval
    end - the end of the interval
    '''

    sum = 0
    for i in range(start, end + 1):
        sum += i
    return sum

async def main():
    start_time = time()
    tasks = []
    for i in range(4):
        task = asyncio.create_task(calculate_sum(i * 250000, (i + 1) * 250000))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    print(f'time: {time() - start_time}')
    print(sum(results))

# if __name__ == "__main__":
#   asyncio.run(main())

if __name__ == "__main__":
        asyncio.run(main())
