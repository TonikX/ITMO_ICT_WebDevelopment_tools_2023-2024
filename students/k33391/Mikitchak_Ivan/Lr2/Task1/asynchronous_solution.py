import time
import asyncio


async def sum_range(l, r, results, ind):
    s = 0
    for i in range(l, r + 1):
        s += i
    results[ind] = s


async def main():
    n = 4  # Number of tasks
    results = [0] * n
    tasks = [None] * n
    
    for i in range(n):
        l = 1 + i * (100_000_000 // n)
        r = (i + 1) * (100_000_000 // n)        
        tasks[i] = asyncio.create_task(sum_range(l, r, results, i))
    
    start = time.time()
    await asyncio.gather(*tasks)
    total_sum = sum(results)
    finish = time.time()
    
    print(f"Sum: {total_sum}\nTime: {finish - start}")
    

if __name__ == "__main__":
    asyncio.run(main())
