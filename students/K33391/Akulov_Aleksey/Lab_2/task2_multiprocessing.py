from multiprocessing import Process, Pool
import requests
from bs4 import BeautifulSoup

def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text if soup.find('title') else 'No title found'
    print(f'Processed {url}: {title}')

def main_multiprocessing(urls):
    with Pool(processes=4) as pool:
        pool.map(parse_and_save, urls)

urls = ['https://example.com', 'https://example.org', 'https://example.net']
main_multiprocessing(urls)
