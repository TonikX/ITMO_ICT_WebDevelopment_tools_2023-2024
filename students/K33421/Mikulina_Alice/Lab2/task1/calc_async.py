import time
import asyncio

async def calculate_sum(start, end):
    total = 0
    for i in range(start, end+1):
        total += i
    return total

async def main():
    calc_end = 4_000_000
    chunk_size = 250000

    num_tasks = calc_end // chunk_size
    
    start_time = time.time()
    
    tasks = []
    for i in range(num_tasks):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        task = asyncio.create_task(calculate_sum(start, end))
        tasks.append(task)
    
    total = 0
    for task in tasks:
        total += await task
    
    end_time = time.time()
    
    formula_result = (calc_end * (calc_end + 1)) // 2
    print(f"Calculation Result: {total}")
    print("Correct result (by formula):", formula_result)
    print("Is result correct:", "yes" if total == formula_result else "no")
    print(f"Calculation time: {(end_time - start_time) * 1000:.3f} ms")

if __name__ == "__main__":
    asyncio.run(main())