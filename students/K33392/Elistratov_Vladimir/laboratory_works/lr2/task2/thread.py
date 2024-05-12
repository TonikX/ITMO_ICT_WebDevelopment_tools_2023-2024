import threading
import requests
from bs4 import BeautifulSoup
from urls import urls
from t2_City import City
from t2_db import add_city

def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.text.strip()
    print("Thread title: ", title)

    city_name_element = soup.select_one("span[class='mw-page-title-main']")
    if city_name_element:
        city_name = city_name_element.text.strip()
    else:
        city_name = "Unknown"

    print("Thread name: ", city_name)


    city_description_element = soup.find("div", class_="mw-content-ltr mw-parser-output").find("p")
    if city_description_element:
        city_description = city_description_element.text.strip()
    else:
        city_description = "Unknown"
    
    print("Thread description: ", city_description, "\n")

    
    try:
        city = City(name=city_name, description=city_description, region_id=1) 
        add_city(city)  
    except Exception as e:
        print(f"Error while adding page: {e}")



def main():
    threads = []

    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print("Execution time (thread):", time.time() - start_time)