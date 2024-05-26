import re
from time import time

import requests
from bs4 import BeautifulSoup

from .db_conn import save_transitions, save_stays


URLS = {
    "planes": "https://buenos-aires-international-airport.com/flights/departures/",
    "cruises": "https://www.cruisecritic.co.uk/find-a-cruise/port-dubrovnik",
    "trains": "https://www.thetrainline.com/",
    "airbnb": "https://www.airbnb.co.uk/?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&search_mode=flex_destinations_search&flexible_trip_lengths%5B%5D=one_week&location_search=MIN_MAP_BOUNDS&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=2&channel=EXPLORE&search_type=category_change&price_filter_num_nights=5&category_tag=Tag%3A8225",
    "hotels": "https://www.booking.com/hotel/index.en-gb.html?aid=397594&label=gog235jc-1BCAEiBWhvdGVsKIICOOgHSDNYA2i2AYgBAZgBCbgBB8gBDdgBAegBAYgCAagCA7gC1I-YsQbAAgHSAiQ4MmE2NmQxMi02MGYwLTQzNzgtOTZjYy0zMDhhZTdiZDhkZmHYAgXgAgE&sid=bec09db0ecce614ac10826c52f468f76",
    "hostels": "https://www.booking.com/hostels/index.en-gb.html?aid=397594&label=gog235jc-1BCAEiBWhvdGVsKIICOOgHSDNYA2i2AYgBAZgBCbgBB8gBDdgBAegBAYgCAagCA7gC1I-YsQbAAgHSAiQ4MmE2NmQxMi02MGYwLTQzNzgtOTZjYy0zMDhhZTdiZDhkZmHYAgXgAgE&sid=bec09db0ecce614ac10826c52f468f76&from_booking_home_promotion=1&",
    }


def parse_planes(soup):
    elems = soup.find_all(class_="menu-item-object-custom")
    names = [r.text.split(' | ') for r in elems if '|' in r.text]
    names = [' '.join(n[1].split()[:-2]) + ', ' + n[0] for n in names]
    return [("Buenos Aires, Argentina", n, "plane") for n in names]


def parse_cruises(soup):
    elems = soup.find_all(class_="css-18jw8gc") 
    return [(e.text, "Dubrovnik, Croatia", 'ship') for e in elems if e.text.isalpha()]


def parse_trains(soup):
    elems = soup.find_all("a", class_="route-suggestions-links")
    texts = [e.text.split() for e in elems[:-5]]
    return [(x[0], x[2], 'train') for x in texts if x[2][0].isupper()]


def parse_airbnb(soup):
    elems = soup.find_all(attrs={"data-testid": "listing-card-title"})
    locations = [e.text for e in elems]
    return [(l, l, 'apartments') for l in locations]
 

def parse_hotels(soup):
    elems = soup.find_all("ul", class_="lp-hotel__explore_world_hotels")
    names = []
    locations = []
    for elem in elems:
        names.extend(elem.find_all("span", class_="bui-list__description-title"))
        locations.extend(elem.find_all("span", class_="bui-list__description-subtitle"))
    names = [n.decode_contents() for n in names]
    locations = [l.decode_contents().split() for l in locations]
    locations = [' '.join(filter(lambda x: re.match("[A-Za-z],?", x), l)) for l in locations]
    pairs = list(zip(locations, names))
    trios = [(p[0], p[1], 'hotel') for p in pairs]
    return trios  


def parse_hostels(soup):
    names = soup.find_all("a", class_="bui-card__title")
    locations = soup.find_all("p", class_="bui-card__subtitle")
    names = [n.text for n in names]
    locations = [l.decode_contents().split() for l in locations]
    locations = [' '.join(filter(lambda x: re.match("[A-Za-z],?", x), l)) for l in locations]
    pairs = list(zip(locations, names))
    trios = [(p[0], p[1], 'hostel') for p in pairs]
    return trios


def parse_and_save(key, url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        if key == "planes":
            data = parse_planes(soup)
            save_transitions(data)
        if key == "cruises": 
            data = parse_cruises(soup)
            save_transitions(data)
        if key == "trains": 
            data = parse_trains(soup)
            save_transitions(data)
        if key == "airbnb":
            data = parse_airbnb(soup)
            save_stays(data)
        if key == "hotels": 
            data = parse_hotels(soup)
            save_stays(data)
        if key == "hostels": 
            data = parse_hostels(soup)
            save_stays(data) 
    except Exception as e:
        print("OH NO, EXCEPTION!")
        raise e