import asyncio

total_sum = 0


async def calculate_sum(left: int, right: int):
    global total_sum
    local_sum = 0
    for i in range(left, right + 1):
        local_sum += i

    total_sum += local_sum


async def main():
    n = int(input("Укажите степень параллелизма "))

    top_border = 1000000
    step = top_border // n

    for i in range(1, n + 1):
        right_border = step * i
        left_border = right_border - step + 1
        t = asyncio.create_task(calculate_sum(left_border, right_border))
        await t

    print("Total sum equal: ", total_sum)

asyncio.run(main())