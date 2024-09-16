import requests
from bs4 import BeautifulSoup

url = 'https://cryptorank.io/all-coins-list'
response = requests.get(url)

urls_list = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    first_ten_cryptos = soup.find_all(class_="sc-39ba2409-1 bgOSTi")
    for crypto in first_ten_cryptos:
        urls_list.append(crypto.get('href'))

    other_cryptos = soup.find_all(class_="loading-name-cell-2")
    for crypto in other_cryptos:
        a = crypto.find('a')
        urls_list.append(a.get('href'))
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")


settings_file_path = "settings.py"
with open(settings_file_path, "w") as file:
    # Write the list to the settings.py file
    file.write("URLS = {}\n".format(urls_list))
