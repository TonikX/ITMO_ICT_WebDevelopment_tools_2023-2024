import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from tflab_2.task2.common.db import save_user



def parse_travel_card(card):
    try:
        name_tag = card.select_one("a.ts-bl-name-link")
        name = name_tag.text.strip() if name_tag else None

        addons = card.select_one("div.ts-bl-addons")
        age, country = None, None
        if addons:
            match = re.match(r"(\d+)\s+лет,\s+(.+?),\s+(.+)", addons.text.strip())
            if match:
                age = int(match.group(1))
                country = match.group(3)

        bio_tag = card.select_one("div.tl-bl-center-trip-right-text-text")
        bio = bio_tag.text.strip() if bio_tag else None

        gender = None
        if card.select_one("div.ts-bl-who-woman[title^='Женщина']"):
            gender = "female"
        elif card.select_one("div.ts-bl-who-man[title^='Мужчина']"):
            gender = "male"

        if not name:
            return None

        fake_email = f"{name.lower().replace(' ', '_')}@example.com"
        fake_password = "default_password"

        return {
            "name": name,
            "email": fake_email,
            "password": fake_password,
            "bio": bio,
            "age": age,
            "gender": gender,
            "country": country,
            "created_at": datetime.utcnow()
        }
    except Exception as e:
        print(f"[ERROR] Ошибка при парсинге карточки: {e}")
        return None


def process_page(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("#ts-blocks-inner .ts-item")

    for card in cards:
        data = parse_travel_card(card)
        if data:
            save_user(data)