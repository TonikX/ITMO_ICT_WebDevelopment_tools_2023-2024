import multiprocessing as mp


def calculate_sum(q, left: int, right: int):
    local_sum = 0
    for i in range(left, right + 1):
        local_sum += i

    total_sum = q.get()
    total_sum += local_sum
    q.put(total_sum)


def main():
    n = int(input("Укажите степень параллелизма "))
    processes = []

    top_border = 1000000
    step = top_border // n

    q = mp.Queue()
    q.put(0)

    for i in range(1, n+1):
        right_border = step*i
        left_border = right_border-step+1
        p = mp.Process(target=calculate_sum, args=(q, left_border, right_border,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total_sum = q.get()
    print("Total sum equal: ", total_sum)


if __name__ == '__main__':
    main()
