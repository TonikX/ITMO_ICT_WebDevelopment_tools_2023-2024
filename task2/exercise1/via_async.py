import asyncio
import math
import time


async def compute_sum(start, end):
    return sum(range(start, end + 1))


async def compute_with_threading(start, end, n_funcs):
    coroutines = []
    step = int(math.ceil((end - start) / n_funcs))
    start_i = start
    while start_i <= end:
        end_i = min(start_i + step, end)
        coroutine = compute_sum(start_i, end_i)
        coroutines.append(coroutine)
        start_i = end_i + 1

    gather_coroutine = asyncio.gather(*coroutines)
    partial_sums = await gather_coroutine
    result_sum = sum(partial_sums)
    return result_sum


async def measure(n_funcs):
    start_time = time.perf_counter()
    res = await compute_with_threading(1, 1000000, n_funcs)
    elapsed = round(time.perf_counter() - start_time, 4)
    print(f"Async functions: {n_funcs}; time: {elapsed}; result: {res}")


async def main():
    n_funcs_list = [1, 5, 10, 20, 50, 100, 1000]
    for n_funcs in n_funcs_list:
        await measure(n_funcs)


if __name__ == "__main__":
    asyncio.run(main())
