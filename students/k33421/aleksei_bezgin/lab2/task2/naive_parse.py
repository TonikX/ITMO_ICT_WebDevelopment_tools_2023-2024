import datetime

import sys
import os
sys.path.append(os.path.expanduser('~/Desktop/ITMO_ICT_WebDevelopment_tools_2023-2024/students/k33421/aleksei_bezgin/lab1/hack_lab/app/db'))
sys.path.append(os.path.expanduser('~/Desktop/ITMO_ICT_WebDevelopment_tools_2023-2024/students/k33421/aleksei_bezgin/lab1/hack_lab/app'))

from connection import engine
from models import Hackathon, Task

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
import json
import time


def add_hackathon(hack_info):
    hack_name, hack_link = hack_info['name'], hack_info['link']
    # спарсили данные про кейс
    inner_page = requests.get(hack_link)
    soup_in = BeautifulSoup(inner_page.text, 'html.parser')
    paragraphs = list(map(lambda x: x.text, soup_in.find_all('p')))
    hack_case = '\n'.join(paragraphs)
    case_title = paragraphs[0]

    with Session(engine) as session:
        hackathon = Hackathon(
            name=hack_name,
            start_date=datetime.datetime.now(),
            # пусть все хакатоны длятся неделю
            end_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        session.add(hackathon)
        session.commit()
        session.refresh(hackathon)

        task = Task(
            title=case_title,
            description=hack_case,
            requirements="Be cool",
            evaluation_criteria="Accuracy",
            hackathon_id=hackathon.id  # Assign the hackathon_id to establish the relationship
        )
        session.add(task)
        session.commit()
        session.refresh(task)


if __name__ == "__main__":
    hack_data = json.load(open('hack_links.json'))

    time_start = time.time()
    for hack_info in hack_data:
        add_hackathon(hack_info)

    print(f'scraped info about {len(hack_data)} events')
    print(f'done in {time.time() - time_start} seconds')