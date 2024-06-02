import requests
import os
from typing import Any, Dict

def add_cities(city_data : Dict[str, Any]) -> bool:
    try:
        api_url = os.getenv("ADD_CITY_URL")
        response = requests.patch(api_url, json=city_data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        return False