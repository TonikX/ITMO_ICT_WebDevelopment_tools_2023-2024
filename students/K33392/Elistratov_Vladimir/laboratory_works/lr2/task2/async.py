import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urls import urls
from t2_db import add_city
from t2_City import City

async def fetch_page(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.text.strip()
        print("Async title: ", title)

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

        return City(name=city_name, description=city_description, region_id=1)

async def parse_and_save(session, url):
    city = await fetch_page(session, url)
    try:
        add_city(city)
    except Exception as e:
        print(f"Error while adding page: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import time
    start_time = time.time()
    asyncio.run(main())
    print("Execution time (async):", time.time() - start_time)