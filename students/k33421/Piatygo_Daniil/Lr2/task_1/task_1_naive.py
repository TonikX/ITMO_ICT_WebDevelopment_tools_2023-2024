from Lr2.mark_time import mark_time


@mark_time
def calculate_sum(n=1000000):
    s = 0
    for i in range(1, n + 1):
        s += i
    return s


if __name__ == "__main__":
    print(calculate_sum())
