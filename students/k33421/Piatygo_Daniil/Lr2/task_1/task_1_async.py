import asyncio
from Lr2.mark_time import mark_time


async def calculate_part_sum(start, end):
    s = 0
    for i in range(start, end + 1):
        s += i
    return s


@mark_time
async def calculate_sum(n=1000000, n_steps=4):
    step = n // n_steps
    ranges = [
        (i * step + 1, n) if i == n_steps - 1 else (i * step + 1, (i + 1) * step)
        for i in range(n_steps)
    ]
    # Создаём задачи для каждого диапазона и собираем результаты
    results = await asyncio.gather(*[calculate_part_sum(*range_) for range_ in ranges])
    return sum(results)


if __name__ == "__main__":
    print(asyncio.run(calculate_sum()))
