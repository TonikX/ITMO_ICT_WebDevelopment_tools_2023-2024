import threading

def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.append(total)

def main():
    result = []
    threads = []
    chunk_size = 100000

    for i in range(0, 1000000, chunk_size):
        thread = threading.Thread(target=calculate_sum, args=(i+1, i+chunk_size+1, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Sum:", sum(result))

if __name__ == "__main__":
    main()

