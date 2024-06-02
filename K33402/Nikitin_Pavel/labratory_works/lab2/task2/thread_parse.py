import threading
import requests
from bs4 import BeautifulSoup
import time
from database import commit_article

def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string
    commit_article(title)


def main():
    urls = ["https://zoom.us/", "https://www.skype.com/", "https://discord.com/"]

    threads = []

    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")