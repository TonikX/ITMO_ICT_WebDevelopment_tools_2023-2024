import threading

total_sum = 0


def calculate_sum(left: int, right: int):
    global total_sum
    local_sum = 0
    for i in range(left, right+1):
        local_sum += i
        
    total_sum += local_sum


def main():
    n = int(input("Укажите степень параллелизма "))
    threads = []

    top_border = 1000000
    step = top_border // n

    for i in range(1, n+1):
        right_border = step*i
        left_border = right_border-step+1
        t = threading.Thread(target=calculate_sum, args=(left_border, right_border,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Total sum equal: ", total_sum)


main()