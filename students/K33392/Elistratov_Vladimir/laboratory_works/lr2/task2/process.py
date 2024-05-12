import multiprocessing
import requests
from bs4 import BeautifulSoup
from urls import urls
from t2_db import add_city
from t2_City import City

def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.text.strip()
    print("Process title: ", title)

    city_name_element = soup.select_one("span[class='mw-page-title-main']")
    if city_name_element:
        city_name = city_name_element.text.strip()
    else:
        city_name = "Unknown"

    print("Process name: ", city_name)


    city_description_element = soup.find("div", class_="mw-content-ltr mw-parser-output").find("p")
    if city_description_element:
        city_description = city_description_element.text.strip()
    else:
        city_description = "Unknown"
    
    print("Process description: ", city_description, "\n")

    
    try:
        city = City(name=city_name, description=city_description, region_id=1) 
        add_city(city)  
    except Exception as e:
        print(f"Error while adding page: {e}")

def main():
    processes = []

    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print("Execution time (process):", time.time() - start_time)