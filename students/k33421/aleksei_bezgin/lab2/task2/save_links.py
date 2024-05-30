import requests
from bs4 import BeautifulSoup
import json

main_link = 'https://hacklist.ru/'
main_page = requests.get(main_link)
soup = BeautifulSoup(main_page.text, 'html.parser')
json_data = []

if __name__ == "__main__":
    # сложили в список, чтобы распараллелить потом
    for part in soup.select('div[class*="jet-listing-grid__item jet-listing-dynamic-post"]'):
        hack_name = part.find('h3').text
        hack_link = part.find('a')['href']
        json_data.append({'name': hack_name, 'link': hack_link})

    json.dump(json_data, open('hack_links.json', 'w'))


