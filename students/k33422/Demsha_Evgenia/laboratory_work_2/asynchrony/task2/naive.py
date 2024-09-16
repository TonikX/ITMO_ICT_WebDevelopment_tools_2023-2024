import requests
from bs4 import BeautifulSoup
from lab1.models import SQLModel, Account
from task2.settings import URLS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
import os
from dotenv import load_dotenv
load_dotenv()


db_url = os.getenv('DB_ADDRESS')
engine = create_engine(db_url)
SQLModel.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def parse(crypto_url):

    url = 'https://cryptorank.io' + crypto_url
    response = requests.get(url)
    name_str, price_int = '', 0

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find(class_="sc-b7cd6de0-0 sc-a4def8f2-9 iYEMqG kqBEPt")
        name_str = name.text.replace('\xa0', '') if name else ''

        price = soup.find(class_="sc-be4b7d84-0 sc-3f59c54e-1 lfEaaA kVlkDl")
        price_str = price.find('div', class_='sc-cb748c3-0 cwWsJH').get_text()
        try:
            price_int = round(float(price_str.replace(',', '')))
        except ValueError:
            price_int = 0
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    return {"name": name_str, "balance": price_int, "user_id": 1}


# Function to populate and send data to the database
def save(parsed_data):
    session = Session()
    try:
        account = Account(**parsed_data)
        session.add(account)
        session.commit()
        print("Data successfully added to the database.")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

    finally:
        session.close()


def parse_and_save(url):
    data = parse(url)
    save(data)


if __name__ == "__main__":
    start_time = time.time()
    for url in URLS[:31]:
        parse_and_save(url)
    print(time.time() - start_time)

