from bs4 import BeautifulSoup
import requests
import aiohttp


def parse_trips(url):
    parsed_trips = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    trips = soup.find_all("div", class_="tour-preview")
    for trip in trips:
        name = trip.find_next('a', class_='tour-preview__title').find_next('span').text.strip()
        price = trip.find_next('div', class_='tour-preview__price').find_next('span').text.strip()[:-2]
        difficulty = len(trip.find_next('span', class_='difficulty-dots__rating') \
                         .find_all('span', class_='difficulty-dots__item difficulty-dots__item--active'))
        comfort = trip.find_next('span', class_='accommodation-comfort-item').text.strip()
        place = trip.find_next('span', class_='tour-preview__photo-region').text.strip().strip('"')
        activities = []
        for activity in trip.find_next('ul', class_='tour-preview__tags').find_all('a', class_='as-tag'):
            activities.append(activity.text.strip().strip('"'))
        parsed_trips.append({
            'name': name,
            'price': price,
            'difficulty': difficulty,
            'comfort': comfort,
            'place': place,
            'activities': activities,
        })
    return parsed_trips

async def parse_trips_async(url):
    parsed_trips = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            response = await res.text()
    soup = BeautifulSoup(response, 'html.parser')
    trips = soup.find_all("div", class_="tour-preview")
    for trip in trips:
        name = trip.find_next('a', class_='tour-preview__title').find_next('span').text.strip()
        price = trip.find_next('div', class_='tour-preview__price').find_next('span').text.strip()[:-2]
        difficulty = len(trip.find_next('span', class_='difficulty-dots__rating') \
                         .find_all('span', class_='difficulty-dots__item difficulty-dots__item--active'))
        comfort = trip.find_next('span', class_='accommodation-comfort-item').text.strip()
        place = trip.find_next('span', class_='tour-preview__photo-region').text.strip().strip('"')
        activities = []
        for activity in trip.find_next('ul', class_='tour-preview__tags').find_all('a', class_='as-tag'):
            activities.append(activity.text.strip().strip('"'))
        parsed_trips.append({
            'name': name,
            'price': price,
            'difficulty': difficulty,
            'comfort': comfort,
            'place': place,
            'activities': activities,
        })
    return parsed_trips
