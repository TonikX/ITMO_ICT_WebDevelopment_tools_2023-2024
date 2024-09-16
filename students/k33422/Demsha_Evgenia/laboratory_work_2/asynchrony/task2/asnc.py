import aiohttp
import asyncio
from bs4 import BeautifulSoup
from task2.settings import URLS
from lab1.models import SQLModel, Account
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()


db_url = os.getenv('DB_ADDRESS')
engine = create_engine(db_url)
SQLModel.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                name = soup.find(class_="sc-b7cd6de0-0 sc-a4def8f2-9 iYEMqG kqBEPt")
                price = soup.find(class_="sc-be4b7d84-0 sc-3f59c54e-1 lfEaaA kVlkDl")
                name_str = name.text.replace('\xa0', '') if name else ''
                price_str = price.find('div', class_='sc-cb748c3-0 cwWsJH').get_text() if price else '0'
                try:
                    price_int = round(float(price_str.replace(',', '')))
                except ValueError:
                    price_int = 0
                return {"name": name_str, "balance": price_int, "user_id": 1}
            else:
                print(f"Failed to fetch data. Status code: {response.status}")
                return {"name": '', "balance": 0, "user_id": 1}


async def save_data(parsed_data):
    with Session() as session:
        try:
            account = Account(**parsed_data)
            session.add(account)
            session.commit()
            print("Data successfully added to the database.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")


async def parse_and_save(url):
    data = await fetch_data('https://cryptorank.io' + url)
    await save_data(data)


async def main(urls):
    tasks = [parse_and_save(url) for url in urls]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()

    asyncio.run(main(URLS[:31]))

    print(time.time() - start_time)
