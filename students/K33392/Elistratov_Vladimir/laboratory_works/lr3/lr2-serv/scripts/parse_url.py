import requests
from bs4 import BeautifulSoup

def parse_url(url: str) -> dict:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": f"Unable to access URL, status code: {response.status_code}"}

        soup = BeautifulSoup(response.content, 'html.parser')

        city_name_element = soup.select_one("span[class='mw-page-title-main']")
        if city_name_element:
            city_name = city_name_element.text.strip()
        else:
            city_name = "Unknown"

        print("Async name: ", city_name)


        city_description_element = soup.find("div", class_="mw-content-ltr mw-parser-output").find("p")
        if city_description_element:
            city_description = city_description_element.text.strip()
        else:
            city_description = "Unknown"
        
        print("Async description: ", city_description, "\n")

        return {"name": city_name, "description": city_description, "region_id": 1}

    except Exception as e:
        return {"error": str(e)}