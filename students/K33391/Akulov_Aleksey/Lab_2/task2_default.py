import time

from common import URLS, parse_and_save

def main(urls):
    for url in urls:
        parse_and_save(url)

if __name__ == "__main__":
    start_time = time.time()
    main(URLS)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Synchronous execution time: {execution_time}")