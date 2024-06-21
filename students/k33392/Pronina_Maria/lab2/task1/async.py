import asyncio
import time


async def calculate_sum(start_num, end_num):
    return sum(range(start_num, end_num))


async def main():
    n = 5
    total = 1000000
    chunk_size = total // n
    tasks = list()

    for i in range(n):
        start_num = i * chunk_size + 1
        end_num = (i + 1) * chunk_size + 1
        task = asyncio.create_task(calculate_sum(start_num, end_num))
        tasks.append(task)

    result = await asyncio.gather(*tasks)

    return sum(result)


if __name__ == "__main__":
    start_time = time.time()
    total_sum = asyncio.run(main())
    result_time = time.time() - start_time
    print(f'Sum: {total_sum} \nTime: {result_time}')
