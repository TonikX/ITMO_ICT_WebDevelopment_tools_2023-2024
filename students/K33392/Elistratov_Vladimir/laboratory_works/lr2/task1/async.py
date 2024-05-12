import asyncio
from asyncio import Semaphore
import nest_asyncio

nest_asyncio.apply()

sm = 0

async def func(semaphore):
    global sm
    async with semaphore:   
        for i in range(1000000):
            sm = sm + i
    return "Done"


async def main():
    semaphore = Semaphore(1)
    tasks = [asyncio.create_task(func(semaphore)) for _ in range(10)]
    result = await asyncio.gather(*tasks)
    print(sm)
    #print(result)
        

loop = asyncio.get_event_loop()
loop.run_until_complete(main())