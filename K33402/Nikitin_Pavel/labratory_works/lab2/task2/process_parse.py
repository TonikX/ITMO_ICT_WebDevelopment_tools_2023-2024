import multiprocessing
import requests
from bs4 import BeautifulSoup
import time
from database import commit_article

def parse_and_save(url):
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text, 'html.parser')
    title = parsed_html.title.string
    commit_article(title)


def main():
    urls = ["https://zoom.us/", "https://www.skype.com/", "https://discord.com/"]

    processes = []

    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")