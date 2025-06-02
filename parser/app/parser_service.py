import asyncio
import re
from datetime import datetime, timedelta

import aiohttp
from bs4 import BeautifulSoup

from db.db_saver import save_user_async


async def fetch(session, url):
    async with session.get(url, timeout=10, ssl=False) as response:
        text = await response.text()
        return url, text

async def parse_and_save(url):
    async with aiohttp.ClientSession() as session:
        url, html = await fetch(session, url)
        if html:
            await process_page_async(html)


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


async def process_page_async(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("#ts-blocks-inner .ts-item")

    tasks = []
    for card in cards:
        data = parse_travel_card(card)
        if data:
            tasks.append(save_user_async(data))
    await asyncio.gather(*tasks)
