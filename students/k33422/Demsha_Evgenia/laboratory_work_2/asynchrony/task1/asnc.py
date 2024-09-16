import asyncio
import time
import os
from dotenv import load_dotenv


async def calculate_sum(start, end, results, res_id):
    curr_sum = 0
    for num in range(start, end+1):
        curr_sum += num
    print(f'task {res_id}, result {curr_sum}')
    results[res_id] = curr_sum
    # await asyncio.sleep(2)

load_dotenv()
num_workers = int(os.getenv('NUM_WORKERS'))
amount = int(os.getenv('AMOUNT'))
load = amount // num_workers

result_list = [None] * num_workers

start_time = time.time()

async def main():
    tasks = [calculate_sum((strt := i*load), strt + load, result_list, i) for i in range(num_workers)]
    await asyncio.gather(*tasks)

asyncio.run(main())

print(sum(result_list))
print(time.time() - start_time)
